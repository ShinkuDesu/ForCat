from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import UnmappedInstanceError

from ..database.database import get_session
from ..crud.message import MessageCrud
from ..crud.thread import ThreadCrud
from ..models.message import *
from ..models.thread import *
from config import *

router = APIRouter(
    prefix='/thread',
    tags=['Thread']
)

@router.get('/{thread_id}', response_model=ThreadRead)
async def get_thread_by_id(thread_id: int, session: AsyncSession = Depends(get_session)) -> ThreadTable:
    result = await ThreadCrud(session).get_thread_by_id(thread_id)
    if not result:
        raise HTTPException(404, 'Thread not found.')
    return result


@router.get('/messages/{thread_id}', response_model=ThreadReadWithMessages)
async def get_thread_with_messages(thread_id: int, offset: int = 0, limit: int = THREAD_MESSAGE_STANDART_LIMIT, session: AsyncSession = Depends(get_session)) -> ThreadTable:
    result = await ThreadCrud(session).get_thread_by_id_with_messages(thread_id, offset, limit)
    if not result:
        raise HTTPException(404, 'Thread not found.')
    return result


@router.post('/', response_model=ThreadRead)
async def create_thread(data: ThreadCreate, session: AsyncSession = Depends(get_session)) -> ThreadTable:
    return await ThreadCrud(session).create_thread(data)


@router.patch('/{thread_id}', response_model=ThreadRead)
async def update_thread_by_id(thread_id: int, data: ThreadUpdate, session: AsyncSession = Depends(get_session)) -> ThreadTable:
    try:  
        return await ThreadCrud(session).update_thread(thread_id, data)
    except UnmappedInstanceError:
        raise HTTPException(404, 'Thread not found.')


@router.delete('/{thread_id}')
async def delete_thread_by_id(thread_id: int, session: AsyncSession = Depends(get_session)) -> dict:
    if not await ThreadCrud(session).delete_thread_by_id(thread_id):
        raise HTTPException(404, 'Thread not found.')
    return {'ok': True}

