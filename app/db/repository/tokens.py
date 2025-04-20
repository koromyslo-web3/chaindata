from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from ..engine import UnitOfWork
from ..orm import OrmToken
from ...utils.funcs import exclude_none_from_kwargs


async def get_many(**kwargs):
    filters = exclude_none_from_kwargs(**kwargs)
    async with UnitOfWork(commit=False) as session:
        stmt = select(
            OrmToken.symbol,
            OrmToken.contract,
            OrmToken.decimals,
            OrmToken.network_id,
        ).filter_by(**filters)
        q = await session.execute(stmt)
        return q.mappings().all()


async def create(symbol, contract, decimals, network_id):
    async with UnitOfWork() as session:
        stmt = (
            insert(OrmToken)
            .values(
                symbol=symbol,
                contract=contract,
                decimals=decimals,
                network_id=network_id,
            )
            .on_conflict_do_nothing(index_elements=["contract", "network_id"])
            .returning(OrmToken.id)
        )

        result = await session.execute(stmt)
        inserted_id = result.scalar()

        return inserted_id is not None
