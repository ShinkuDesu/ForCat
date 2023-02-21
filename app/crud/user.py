from sqlalchemy import select

from crud.base import CrudBase
from models import user


class UserCrud(CrudBase):
    async def get_user_by_id(self, user_id: int) -> user.UserTable | None:
        return await self._session.get(user.UserTable, user_id)
    
    async def get_user_by_email(self, user_id: int) -> user.UserTable | None:
        return await self._session.get(user.UserTable, user_id)

    async def get_user_by_username(self, username: str) -> user.UserTable | None:
        stmt = select(user.UserTable).where(user.UserTable.username == username)
        result = await self._session.execute(stmt)
        return result.scalar()

    async def create_user(self, data: user.UserCreate) -> user.UserTable |  None:
        db_user = user.UserTable(
            username=data.username,
            email=data.email,
            image_url = data.image_url,
            hashed_password = data.password + 'hashe',
            )
        self._session.add(db_user)
        await self._session.commit()
        await self._session.refresh(db_user)
        return db_user
