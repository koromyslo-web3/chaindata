from fastapi import APIRouter, Body
from ..core import Transaction

router = APIRouter()

@router.post("/send")
async def send(
    transaction: Transaction = Body()
):
    await transaction.sign()