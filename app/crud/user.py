from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload, joinedload

from ..crud.base import CrudBase
from ..models.user import *
from ..security import user_auth


class UserCrud(CrudBase):
    async def get_user_by_id(self, id_: int) -> UserTable | None:
        return await self._session.get(UserTable, id_)
    
    async def get_user_by_email(self, user_email: int) -> UserTable:
        result = await self._session.scalar(
            select(UserTable)
            .where(UserTable.email == user_email)
        )
        return result

    async def get_user_by_username(self, username: str) -> UserTable:
        result = await self._session.scalar(
            select(UserTable)
            .where(UserTable.username == username)
        )
        return result

    async def create_user(self, data: UserCreate) -> UserTable:
        hashed_password = user_auth.get_password_hash(data.password)
        result = await self._session.scalar(
            insert(UserTable)
            .values(
                **data.dict(exclude={'password'}),
                hashed_password=hashed_password
            )
            .returning(UserTable)
        )
        await self._session.commit()
        await self._session.refresh(result)
        return result
    
    async def delete_user_by_id(self, id_: int) -> bool:
        result = await self._session.execute(
            delete(UserTable)
            .where(UserTable.id == id_)
        )
        if not result.__dict__.get('rowcount'):
            return False
        await self._session.commit()
        return True
