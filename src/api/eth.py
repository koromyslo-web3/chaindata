from fastapi import APIRouter, Body
from uuid import UUID
from typing import Optional
from src.interfaces.evm import NULL_ADDRESS, Ethereum, EVMError
from src.core.transaction import TransactionBase, Transaction

router = APIRouter()

evm = Ethereum({"default": "https://base.meowrpc.com"})


async def _safe_request(evm_cour):
    try:
        data = await evm_cour
        return {"success": True, "result": data}
    except EVMError as e:
        return {"success": False, "error": e.response}


@router.post("/call")
async def call(
    network_id: str = Body(),
    from_: Optional[str] = Body(NULL_ADDRESS, alias="from"),
    to: str = Body(),
    data: Optional[str] = Body(),
    block: Optional[str] = Body("latest"),
):
    return await _safe_request(evm.call(from_, to, data, block))


@router.post("/logs")
async def get_logs(
    network_id: str = Body(),
    from_block: str | None = Body("latest", alias="fromBlock"),
    to_block: str | None = Body("latest", alias="toBlock"),
    address: list[str] | str | None = Body(None),
    topics: list[str] = Body(None),
):
    return await _safe_request(evm.getLogs(from_block, to_block, address, topics))


@router.post("/transaction")
async def send_transaction(transaction: TransactionBase):
    return await _safe_request(transaction.send())


@router.get("/transaction/estimate")
async def estimate_transaction(transaction: TransactionBase):
    return await _safe_request(transaction.estimate())

@router.get("/transation/{id}")
async def get_transaction(id: UUID):
    return await Transaction.get(id=id)