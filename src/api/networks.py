from fastapi import APIRouter, Query
from ..db import repository

router = APIRouter()

@router.get("")
async def get_network(
    network_id: str = Query()
):
    return await repository.networks.get(id=network_id)