import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

url = f"{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
db_url = "postgresql+asyncpg://" + url
db_sync_url = "postgresql://" + url

engine = create_async_engine(
    db_url, 
    echo=False, 
    future=True
)

Session = sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)


class UnitOfWork:
    def __init__(self, commit=True, session_factory=Session):
        self.session_factory = session_factory
        self.commit = commit

    async def __aenter__(self):
        self.session = self.session_factory()
        return self.session

    async def __aexit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is None and self.commit:
                await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            detail = str(e.orig.args[0])
            raise ValueError(detail.split("\n")[1])
        finally:
            await self.session.close()

