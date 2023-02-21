from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import UnmappedInstanceError
from database.database import get_session

from crud.message import MessageCrud
from models.message import *
from models.thread import *


router = APIRouter(
    prefix='/message',
    tags=['Message']
)


@router.get('/{message_id}', response_model=MessageRead)
async def get_message_by_id(message_id: int, session: AsyncSession = Depends(get_session)) -> MessageTable:
    result = await MessageCrud(session).get_mesage_by_id(message_id)
    if not result:
        raise HTTPException(404, 'Message not found.')
    return result

@router.post('/', response_model=MessageRead)
async def create_message(data: MessageCreate, session: AsyncSession = Depends(get_session)) -> MessageTable:
    return await MessageCrud(session).create_message(data)


@router.patch('/{message_id}', response_model=MessageRead)
async def update_message_by_id(message_id: int, message: MessageUpdate, session: AsyncSession = Depends(get_session)):
    try:  
        return await MessageCrud(session).update_message(message_id, message)
    except UnmappedInstanceError:
        raise HTTPException(404, 'Message not found.')


@router.delete('/{message_id}', response_model=ThreadRead)
async def delete_message_by_id(message_id: int, session: AsyncSession = Depends(get_session)):
    return await MessageCrud(session).delete_message_by_id(message_id)
