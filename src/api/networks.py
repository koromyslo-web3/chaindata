from fastapi import APIRouter, Query
from ..interfaces.db import repository

router = APIRouter()


@router.get("")
async def get_networks():
    return await repository.networks.get_many("id", "name", "type", "native_symbol", "meta")


@router.get("/{id}")
async def get_network(id: str):
    return await repository.networks.get(id=id)
