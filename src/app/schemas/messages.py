from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer

class MessageBase(BaseModel):
    message_id: UUID = Field(..., alias="message_id")
    chat_id: UUID = Field(..., alias="chat_id")
    content: str
    rating: int
    sent_at: datetime
    role: str

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    content: Optional[str] = None
    rating: Optional[bool] = None
    role: Optional[str] = None

class MessageInDBBase(MessageBase):
    class Config:
        orm_mode = True

