from sqlalchemy import select

from ..engine import UnitOfWork
from ..orm import OrmNetwork
from ...utils.funcs import exclude_none_from_kwargs


async def get(**kwargs) -> dict | None:
    filters = exclude_none_from_kwargs(**kwargs)
    async with UnitOfWork() as session:
        stmt = (
            select(
                OrmNetwork.id,
                OrmNetwork.name,
                OrmNetwork.native_symbol,
                OrmNetwork.type,
                OrmNetwork.endpoints,
            )
            .filter_by(is_active=True, **filters)
        )
        q = await session.execute(stmt)
        return q.mappings().all()
    

    
