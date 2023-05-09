from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from datetime import datetime
from typing import TYPE_CHECKING

from database.database import Base


if TYPE_CHECKING:
    from .message import MessageTable
    from .user import UserTable


class ThreadTable(Base):
    __tablename__ = 'thread'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str | None] = mapped_column(String(2048))
    image_url: Mapped[str| None] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.utcnow)
    
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    
    created_by: Mapped['UserTable'] = relationship(back_populates='threads')
    messages: Mapped[list['MessageTable']] = relationship(back_populates='thread')


class ThreadBase(BaseModel):
    title: str = Field(max_length=256)
    description: str  = Field(max_lenght=2048)
    image_url: str = Field(max_lenght=256)


class ThreadRead(ThreadBase):
    id: int = Field(primary_key=True)
    created_at: datetime
    updated_at: datetime | None

    created_by: 'UserRead'

    class Config:
        orm_mode = True


class ThreadCreate(ThreadBase):
    user_id: int = Field(gt=0)


class ThreadUpdate(ThreadBase):
    title: str | None = Field(max_length=256)
    description: str | None  = Field(max_lenght=2048)
    image_url: str | None = Field(max_lenght=256)


class ThreadReadWithMessages(ThreadRead):
    messages: list['MessageRead']


from .message import MessageRead
from .user import UserRead

ThreadRead.update_forward_refs()
