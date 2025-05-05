from sqlalchemy import select

from ..engine import UnitOfWork
from ..orm import OrmNetwork
from ....utils.funcs import exclude_none_from_kwargs


async def _get_mappings_first(stmt) -> dict:
    async with UnitOfWork() as session:
        q = await session.execute(stmt)
        return q.mappings().first()


async def get_one(*args, **kwargs) -> dict:
    fields = (getattr(OrmNetwork, arg) for arg in args)
    stmt = select(*fields).filter_by(is_active=True, **kwargs)
    return await _get_mappings_first(stmt)


async def get(**kwargs) -> dict | None:
    filters = exclude_none_from_kwargs(**kwargs)
    async with UnitOfWork() as session:
        stmt = select(
            OrmNetwork.id,
            OrmNetwork.name,
            OrmNetwork.native_symbol,
            OrmNetwork.type,
            OrmNetwork.endpoints,
        ).filter_by(is_active=True, **filters)
        q = await session.execute(stmt)
        return q.mappings().all()
