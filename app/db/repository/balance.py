from sqlalchemy import select

from ..engine import UnitOfWork
from ..orm import OrmBalance


async def update(address: str, token_id: str, delta: str):
    delta = int(str)
    async with UnitOfWork(commit=True) as uow:
        stmt = (
            select(OrmBalance)
            .where(OrmBalance.address == address, OrmBalance.token_id == token_id)
            .with_for_update()
        )
        q = await uow.execute(stmt)
        balance: OrmBalance | None = q.scalars().first()

        if balance:
            balance.amount += delta
            return balance.amount

        balance = OrmBalance(address=address, token_id=token_id, amount=delta)
        uow.add(balance)
        return delta


async def get(address: str, token_id: str) -> str:
    async with UnitOfWork(commit=False) as session:
        stmt = select(OrmBalance.amount).filter_by(address=address, token_id=token_id)
        q = await session.execute(stmt)
        return q.scalars().first()
