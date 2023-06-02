from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.database import get_session
from ..models.user import *
from ..crud.user import UserCrud


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.get('/@{username}', response_model=UserRead)
async def get_user_by_username(username: str, session: AsyncSession = Depends(get_session)) -> UserTable:
    result = await UserCrud(session).get_user_by_username(username)
    if not result:
        raise HTTPException(404, 'User not found.')
    return result


@router.get('/{id}', response_model=UserRead)
async def get_user_by_id(id: int, session: AsyncSession = Depends(get_session)) -> UserTable:
    result = await UserCrud(session).get_user_by_id(id)
    if not result:
        raise HTTPException(404, 'User not found.')
    return result


@router.post('/', response_model=UserRead)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)) -> UserTable:
    if await UserCrud(session).get_user_by_email(user.email):
        raise HTTPException(403, 'Email is busy.')
    if await UserCrud(session).get_user_by_username(user.username):
        raise HTTPException(403, 'Username is busy.')
    result = await UserCrud(session).create_user(user)
    if not result: raise HTTPException(404, 'User not found.')
    return result


@router.delete('/{id}')
async def delete_user_by_id(id: int, session: AsyncSession = Depends(get_session)) -> dict:
    if not await UserCrud(session).delete_user_by_id(id):
        raise HTTPException(404, 'User not found.')
    return {'ok': True}
