from fastapi import Depends, HTTPException, Security, status, APIRouter, Response
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import UserCrud
from database.database import get_session
from config import SECRET_KEY, ALGORITHM
from auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from database import models


router = APIRouter()


@router.post("/token", response_model=models.Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
    ):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/status/")
async def read_system_status(current_user: models.User = Depends(get_current_user)):
    return {"status": "ok"}
