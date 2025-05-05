from fastapi import APIRouter, Query, Response, Depends

from ..interfaces.db import repository
from ..config import auth

router = APIRouter()


@router.get("")
async def get_tokens(
    network_id: str | None = Query(None),
    symbol: str | None = Query(None),
    contract: str | None = Query(None),
    decimals: str | None = Query(None),
    service: str = Depends(auth.auth),
):
    return await repository.tokens.get_many(
        network_id=network_id, symbol=symbol, contract=contract, decimals=decimals
    )


@router.post("")
async def create_token(
    network_id: str | None = Query(None),
    symbol: str | None = Query(None),
    contract: str | None = Query(None),
    decimals: str | None = Query(None),
    service: str = Depends(auth.auth),
):
    created = await repository.tokens.create(symbol, contract, decimals, network_id)
    return Response(status_code=201 if created else 200)
