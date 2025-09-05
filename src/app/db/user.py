from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from uuid import UUID
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)

    messages = relationship('Message', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"