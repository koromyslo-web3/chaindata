from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from ..interfaces.db import repository
from ..interfaces.services import Wallets
from ..utils.funcs import to_checksum


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

    def txn_dict(self):
        return self.model_dump(by_alias=True, exclude=["id"])

    async def sign(self):
        self._signed = await Wallets.sign(self.txn_dict())

    async def send(self):
        pass

    async def create(self):
        self.id = await repository.transactions.create_transaction(
            self.network_id,
        )
