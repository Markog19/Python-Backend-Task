from fastapi import HTTPException
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from functools import lru_cache

from src.app.api.dependencies import get_current_user, get_db
from src.app.schemas.messages import MessageBase, MessageCreate
from src.app.schemas.user import UserBase
from src.app.services.message_service import MessageService


router = APIRouter()


@lru_cache(maxsize=128)
def get_messages_cached(user_id: str):
    # This function should be pure and not depend on db session directly
    # so this is a demo; for real use, use a cache like Redis or a custom solution
    # This will not work with SQLAlchemy session objects as arguments
    # Instead, you should cache at the service or repository layer
    pass

@router.post("/")
def create_message(message: MessageCreate, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    try:
        message_service = MessageService(db)
        message_service.send_message(message, current_user.id)
        return {"message": "Message sent successfully"}
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/", response_model=List[MessageBase])
def get_messages(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    try:
        # lru_cache cannot cache SQLAlchemy objects or sessions, so we cache by user_id only
        # and fetch from DB each time, but you can cache IDs or serializable data
        message_service = MessageService(db)
        messages = message_service.get_messages(current_user.id)
        if not messages:
            raise HTTPException(status_code=404, detail="No messages found")
        return messages
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{message_id}", response_model=MessageBase)
def update_message(message_id: str, message: MessageBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    try:
        message_service = MessageService(db)
        updated_message = message_service.update_message(message_id, message, current_user.id)
        if not updated_message:
            raise HTTPException(status_code=404, detail="Message not found")
        return updated_message
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")