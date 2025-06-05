from sqlalchemy import select, update

from ..engine import UnitOfWork
from ..orm import OrmTransaction


async def create_transaction(network_id: str, request_data: dict):
    async with UnitOfWork(autocommit=True) as session:
        obj = OrmTransaction(
            network_id=network_id,
            request_data=request_data,
            status="Created"
        )
        session.add(obj)

    return obj.id


async def update_transaction(id, **kwargs):
    async with UnitOfWork(autocommit=True) as session:
        stmt = update(OrmTransaction).where(OrmTransaction.id == id).values(**kwargs)
        await session.execute(stmt)

async def _get_mappings_first(stmt) -> dict:
    async with UnitOfWork() as session:
        q = await session.execute(stmt)
        return q.mappings().first()


async def get_one(*args, **kwargs) -> dict:
    fields = (getattr(OrmTransaction, arg) for arg in args)
    stmt = select(*fields).filter_by(is_active=True, **kwargs)
    return await _get_mappings_first(stmt)