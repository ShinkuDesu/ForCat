from sqlalchemy import select, update, delete, Result, insert
from sqlalchemy.orm import selectinload, joinedload

from crud.base import CrudBase
from models.message import *
from models.thread import *
from models.user import *


class ThreadCrud(CrudBase):
    async def get_thread_by_id(self, id_: int) -> ThreadTable | None:
        return await self._session.scalar(
            select(ThreadTable)
            .where(ThreadTable.id == id_)
            .options(joinedload(ThreadTable.created_by))
        )
    
    async def create_thread(self, data: ThreadCreate) -> ThreadTable:
        result = await self._session.scalar(
            insert(ThreadTable)
            .values(**data.dict())
            .returning(ThreadTable)
            .options(joinedload(ThreadTable.created_by))
        )
        await self._session.commit()
        await self._session.refresh(result)
        return result
    
    async def update_thread(self, id_: int, data: ThreadUpdate) -> ThreadTable:
        result = await self._session.scalar(
            update(ThreadTable)
            .where(ThreadTable.id == id_)
            .values(**data.dict(exclude_unset=True))
            .returning(ThreadTable)
            .options(joinedload(ThreadTable.created_by))
        )
        await self._session.commit()
        await self._session.refresh(result)
        return result

    async def delete_thread_by_id(self, id_: int) -> bool:
        result = await self._session.execute(
            delete(ThreadTable)
            .where(ThreadTable.id == id_)
        )
        if not result.__dict__.get('rowcount'):
            return False
        await self._session.commit()
        return True