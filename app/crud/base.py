from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update, Result, select, ScalarResult, Table, insert
from sqlalchemy.orm import DeclarativeBase, joinedload


class CrudBase:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def _insert(self, table, values: dict, *options):
        result = await self._session.scalar(
            insert(table)
            .values(values)
            .returning(table)
            .options(*options)
        )
        await self._session.commit()
        await self._session.refresh(result)
        return result
