from slowapi import Limiter
from fastapi import Request


from fastapi import HTTPException
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.api.dependencies import get_current_user, get_db
from src.app.schemas.messages import MessageBase, MessageCreate, MessageRead
from src.app.schemas.user import UserBase
from src.app.services.message_service import MessageService

def user_id_key_func(request: Request):
    user = getattr(request.state, "user", None)
    return str(user.id) if user and hasattr(user, "id") else request.client.host

limiter = Limiter(key_func=user_id_key_func)
router = APIRouter()

@router.post("/")
@limiter.limit("1/minute")  
async def create_message(message: MessageCreate, request: Request, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    message_service = MessageService(db)
    message_service.send_message(message, current_user.id)
    return {"message": "Message sent successfully"}


@router.get("/", response_model=List[MessageRead])
@limiter.limit("10/minute") 
async def get_messages(request: Request, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
        message_service = MessageService(db)
        messages = message_service.get_messages(current_user.id)
        if not messages:
            raise HTTPException(status_code=404, detail="No messages found" )
        return messages
    
    
@router.put("/{message_id}", response_model=MessageBase)
@limiter.limit("3/minute")  
async def update_message(message_id: str, message: MessageBase, request: Request, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    
    message_service = MessageService(db)
    updated_message = message_service.update_message(message_id, message, current_user.id)
    if not updated_message:
        raise HTTPException(status_code=404, detail="Message not found")
    return updated_message
