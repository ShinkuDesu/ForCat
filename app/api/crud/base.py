from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update, Result, select, ScalarResult, Table, insert
from sqlalchemy.orm import DeclarativeBase, joinedload


class CrudBase:
    def __init__(self, session: AsyncSession):
        self._session = session
