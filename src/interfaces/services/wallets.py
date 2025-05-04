from .base import BaseService
from typing import NewType

Address = NewType("Address", str)


class WalletService(BaseService):

    async def new(self, amount=1):
        payload = {"amount": amount}
        return await self._request("POST", "/new", json=payload)

    async def sign(self, data: dict):
        return await self._request("POST", "/sign", json=data)
