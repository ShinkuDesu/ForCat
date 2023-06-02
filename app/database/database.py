from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


from ..config import DB_URL


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DB_URL, connect_args={"check_same_thread": False}, echo=True)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session