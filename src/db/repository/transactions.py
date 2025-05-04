from ..orm import OrmTransaction
from ..engine import UnitOfWork
from sqlalchemy import update


async def create_transaction(network_id: str, txn_hash: str, request_data: dict):
    async with UnitOfWork(autocommit=True) as session:
        obj = OrmTransaction(
            network_id=network_id,
            txn_hash=txn_hash,
            request_data=request_data,
        )
        session.add(obj)

    return obj.id


async def update_transaction(id, **kwargs):
    async with UnitOfWork(autocommit=True) as session:
        stmt = update(OrmTransaction).where(OrmTransaction.id == id).values(**kwargs)
        await session.execute(stmt)
