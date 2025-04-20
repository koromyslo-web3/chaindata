from fastapi import APIRouter, Query, Response

from ..db import repository

router = APIRouter()


@router.get("")
async def get_tokens(
    network_id: str | None = Query(None),
    symbol: str | None = Query(None),
    contract: str | None = Query(None),
    decimals: str | None = Query(None),
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
):
    created = await repository.tokens.create(symbol, contract, decimals, network_id)
    return Response(status_code=201 if created else 200)
