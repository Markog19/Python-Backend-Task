

from fastapi import HTTPException
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.api.dependencies import get_current_user, get_db
from src.app.schemas.messages import MessageBase, MessageCreate
from src.app.schemas.user import UserBase
from src.app.services.message_service import MessageService


router = APIRouter()

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
        message_service = MessageService(db)
        messages = message_service.get_messages(current_user.id)
        if not messages:
            raise HTTPException()
        return messages
    except HTTPException as e:
        raise e
    
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