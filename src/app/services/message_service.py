import datetime
from src.app.db.message import Message
from src.app.schemas.messages import MessageCreate


class MessageService:
    def __init__(self, db_session):
        self.db_session = db_session

    def send_message(self, message_data:MessageCreate):

        new_message = Message(
            user_id=message_data.user_id,
            content=message_data.content,
            sent_at=message_data.datetime or datetime.datetime.now(),
            message_id=message_data.message_id,
            chat_id=message_data.chat_id,
            rating=message_data.rating,
            role=message_data.role
            
        )
        self.db_session.add(new_message)
        self.db_session.commit()
        self.db_session.refresh(new_message)
        return new_message

    def get_message(self, user_id):
        return self.db_session.query(Message).filter(Message.user_id == user_id).first()