from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer
from .base import Base

class Message(Base):
    __tablename__ = 'messages'

    message_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    chat_id: Mapped[UUID]
    content: Mapped[str]
    rating: Mapped[int]
    sent_at: Mapped[datetime]
    role: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))

    user = relationship('User', back_populates='messages')