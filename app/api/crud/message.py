from sqlalchemy import select, update, delete, Result, insert
from sqlalchemy.orm import selectinload, joinedload

from ..crud.base import CrudBase
from ..models.message import *
from ..models.thread import *


class MessageCrud(CrudBase):
    async def get_mesage_by_id(self, id_: int) -> MessageTable | None:
        return await self._session.scalar(
                select(MessageTable)
                .where(MessageTable.id == id_)
                .options(joinedload(MessageTable.sent_by))
            )

    async def create_message(self, data: MessageCreate) -> MessageTable:
        result = await self._session.scalar(
            insert(MessageTable)
            .values(**data.dict())
            .returning(MessageTable)
            .options(joinedload(MessageTable.sent_by))
        )
        await self._session.commit()
        await self._session.refresh(result)
        return result
  
    async def update_message(self, id_: int, data: MessageUpdate) -> MessageTable:
        result = await self._session.scalar(
            update(MessageTable)
            .where(MessageTable.id == id_)
            .values(**data.dict(exclude_unset=True))
            .returning(MessageTable)
            .options(joinedload(MessageTable.sent_by))
        )
        await self._session.commit()
        await self._session.refresh(result)
        return result

    async def delete_message_by_id(self, id_: int) -> ThreadTable:
        result = await self._session.scalar(
            delete(MessageTable)
            .where(MessageTable.id == id_)
            .returning(MessageTable.thread_id)
        )
        thread = await self._session.get(ThreadTable, result)
        await self._session.commit()
        return thread
