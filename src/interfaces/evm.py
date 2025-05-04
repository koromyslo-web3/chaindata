from httpx import AsyncClient
from asyncio import sleep


class EVMError(Exception):
    pass


class TransactionTimeout(EVMError):
    pass


class Ethereum:

    __endpoints: dict

    def __init__(self, rpc_endpoints: dict) -> None:
        self.__endpoints = rpc_endpoints

    def _get_endpoint(self, method):
        return self.__endpoints.get(method) or self.__endpoints["default"]

    async def __request(self, method: str, params: list[dict]):
        headers = {"Content-Type": "application/json"}
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1,
        }
        endpoint = self._get_endpoint(method)
        async with AsyncClient() as c:
            response = await c.post(endpoint, headers=headers, json=payload, timeout=60)
            data: dict = response.json()
            if "result" in data.keys():
                return data["result"]
            raise EVMError(data["error"])

    async def getLogs(
        self,
        from_block="latest",
        to_block="latest",
        address: str | list[str] = None,
        topics: list[str] = None,
    ):
        params = [
            {
                "fromBlock": from_block,
                "toBlock": to_block,
                "topics": topics,
                "address": address,
            }
        ]
        return await self.__request("eth_getLogs", params)

    async def getReceipt(self, txn_hash: str):
        params = [txn_hash]
        return await self.__request("eth_getTransactionReceipt", params)

    async def getTransactionByHash(self, txn_hash: str):
        params = [txn_hash]
        return await self.__request("eth_getTransactionByHash", params)

    async def getBlockNumber(self: str):
        res = await self.__request("eth_blockNumber", [])
        return int(res, 16)

    async def getCode(self, address: str):
        params = [address, "latest"]
        return await self.__request("eth_getCode", params)

    async def sendRawTransaction(self, signed_data: str, _id: int = 1):
        return await self.__request("eth_sendRawTransaction", [signed_data], _id)

    async def getNonce(self, address: str) -> int:
        res = await self.__request("eth_getTransactionCount", [address, "latest"])
        return int(res, 16)

    async def waitForTxn(
        self, txn_hash: str, gap: float = 2, timeout: int = 120
    ):
        waited = 0
        while waited < timeout:
            receipt = await self.getReceipt(txn_hash)
            if receipt:
                return receipt
            await sleep(gap)
            waited += gap
        raise TransactionTimeout()
