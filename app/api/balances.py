from fastapi import APIRouter
from ..db import repository

router = APIRouter()


@router.get("")
async def get_balance(
    address: str,
    token_id: str,
):
    current_balance = await repository.balance.get(address, token_id)
    return {"balance": current_balance}


@router.post("")
async def update_balance(address: str, token_id: str, delta: str | int):
    current_balance = await repository.balance.update(address, token_id, int(delta))
    return {"balance": current_balance}
