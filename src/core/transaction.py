from uuid import UUID

from pydantic import BaseModel, Field

from ..interfaces.db import repository
from ..interfaces.evm import Ethereum
from ..config import wallets_service


class Transaction(BaseModel):
    id: UUID | None = None
    network_id: str | None = None

    from_: str | None = Field(alias="from", default=None)
    to: str | None = None
    nonce: int | None = None
    gas: int | None = None
    gasPrice: int | None = None
    value: int | None = None
    data: str | None = None

    _signed: str | None = None
    _ethereum: Ethereum | None = None

    async def ethereum(self):
        network_data = await repository.networks.get_one(
            "endpoints", "meta", id=self.network_id
        )
        self._ethereum = Ethereum(network_data["endpoints"])

    def txn_dict(self):
        return self.model_dump(
            by_alias=True, exclude_none=True, exclude=["id", "network_id"]
        )

    async def sign(self):
        self._signed = await wallets_service.sign(self.txn_dict())

    async def estimate(self):
        pass
        # gas = await

    async def send(self):
        pass

    async def create(self):
        self.id = await repository.transactions.create_transaction(
            self.network_id,
        )
