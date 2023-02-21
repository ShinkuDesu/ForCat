from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

from database.database import Base


if TYPE_CHECKING:
    from message import MessageTable
    from thread import ThreadTable


class UserTable(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    username: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(128))
    hashed_password: Mapped[str] = mapped_column()
    image_url: Mapped[str] = mapped_column(String(256))
    is_active: Mapped[bool] = mapped_column(default=False)

    threads: Mapped[list['ThreadTable']] = relationship(back_populates='created_by')
    messages: Mapped[list['MessageTable']] = relationship(back_populates='sent_by')


class UserBase(BaseModel):
    username: str = Field(max_length=64)
    email: str = Field(max_length=128)
    image_url: str = Field(max_length=256)


class UserRead(UserBase):
    id: int
    hashed_password: str
    is_active: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str
    email: str
