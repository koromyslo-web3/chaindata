from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException
from asyncio import create_task

from ..interfaces.db import repository
from ..interfaces.evm import Ethereum, EVMError, TransactionTimeout
from ..config import wallets_service
from ..utils.funcs import to_checksum


class TransactionBase(BaseModel):
    network_id: str
    from_: str = Field(alias="from", default=None)
    to: str | None = None
    value: int | None = None
    data: str | None = None
    nonce: int | None = None
    gasPrice: int | None = None
    gas: int | None = None

    _id: UUID | None = None
    _network: Ethereum | None = None
    _txn_hash: str | None = None

    @field_validator("from_", "to", mode="after")
    @classmethod
    def to_checksum_address(cls, val: str | None):
        if not val:
            return val
        return to_checksum(val)

    async def get_network(self):
        if not self._network:
            data = await repository.networks.get_one("endpoints", id=self.network_id)
            self._network = Ethereum(data["endpoints"])
        return self._network

    def dict(self, estimation=False):
        exclude = (
            ("network_id", "gasPrice", "gas", "nonce")
            if estimation
            else ("network_id",)
        )
        data = self.model_dump(by_alias=True, exclude_none=True, exclude=exclude)
        return data

    async def estimate(self):
        network = await self.get_network()
        self.gas = await network.estimateGas(self.dict(estimation=True))
        return self.gas

    async def prebuild(self):
        network = await self.get_network()
        self.gas = self.gas or await network.estimateGas(self.dict(estimation=True))
        self.nonce = self.nonce or await network.getNonce(self.from_)
        self.gasPrice = self.gasPrice or await network.gasPrice()

    async def build(self):
        await self.prebuild()
        return self.dict()

    async def send(self):
        if self._id:
            raise ValueError("Known transaction.")

        builded = await self.build()
        self._id = await repository.transactions.create_transaction(
            self.network_id, builded
        )

        signed = await wallets_service.sign(builded)
        network = await self.get_network()
        try:
            self._txn_hash = await network.sendRawTransaction(signed)
            await repository.transactions.update_transaction(
                self._id, status="Send", txn_hash=self._txn_hash
            )
        except EVMError as e:
            await repository.transactions.update_transaction(self._id, status="Failed")
            raise HTTPException(400, e.response)

        create_task(self.polling())

        return {"id": self._id, "txnHash": self.txn_hash}

    async def polling(self):
        network = await self.get_network()
        try:
            receipt = await network.waitForTxn(self._txn_hash, timeout=600)
        except TransactionTimeout:
            await repository.transactions.update_transaction(self._id, status="Lost")
            return

        price = int(receipt["effectiveGasPrice"], 0) * int(receipt["gasUsed"], 0)
        await repository.transactions.update_transaction(
            self._id, receipt=receipt, price=price
        )


class Transaction(BaseModel):
    id: UUID
    status: str
    network_id: str
    price: int | None
    txn_hash: str
    request_data: dict
    receipt: dict | None = None

    @classmethod
    async def get(cls, id):
        data = await repository.transactions.get_one(
            "status",
            "network_id",
            "price",
            "txn_hash",
            "request_data",
            "receipt",
            id=id,
        )
        if not data:
            raise HTTPException(404)
        return cls(**data)
