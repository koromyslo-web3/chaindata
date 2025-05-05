from fastapi import APIRouter, Body, Depends
from ..core import Transaction
from ..config import auth

router = APIRouter()


@router.post("/send")
async def send(
    transaction: Transaction = Body(),
    service: str = Depends(auth.auth),
):
    await transaction.sign()
