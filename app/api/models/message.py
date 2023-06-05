from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING
from datetime import datetime

from ..database.database import Base


if TYPE_CHECKING:
    from .thread import ThreadTable
    from .user import UserTable



class MessageTable(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(primary_key=True)

    text: Mapped[str] = mapped_column(String(2048))
    image_url: Mapped[str | None] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    thread_id: Mapped[int] = mapped_column(ForeignKey('thread.id'))

    sent_by: Mapped['UserTable'] = relationship(back_populates='messages')
    thread: Mapped['ThreadTable'] = relationship(back_populates='messages')


class MessageBase(BaseModel):
    text: str = Field(max_length=2048)
    image_url: str | None = Field(max_length=256)


class MessageRead(MessageBase):
    id: int

    thread_id: int
    created_at: datetime
    updated_at: datetime

    sent_by: 'UserRead'

    class Config:
        orm_mode = True


class MessageCreate(MessageBase):
    user_id: int = Field(gt=0)
    thread_id: int = Field(gt=0)


class MessageUpdate(MessageBase):
    text: str | None
    image_url: str | None


from .user import UserRead
from .thread import ThreadRead
MessageRead.update_forward_refs()
