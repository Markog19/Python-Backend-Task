import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime
from src.app.services.message_service import MessageService
from src.app.db.message import Message
from src.app.schemas.messages import MessageCreate
from src.app.db.user import User  
@pytest.fixture
def db_session():
    mock_session = MagicMock()
    # Mock add, commit, refresh
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.refresh = MagicMock()
    # Mock query chain for get_messages
    mock_query = MagicMock()
    mock_query.filter.return_value.all.return_value = [
        Message(user_id=1, content="test", sent_at=datetime.now(), chat_id=uuid4(), rating=1, role="user")
    ]
    mock_query.filter.return_value.first.return_value = Message(user_id=1, content="test", sent_at=datetime.now(), chat_id=uuid4(), rating=1, role="user")
    mock_session.query.return_value = mock_query
    return mock_session

def test_send_message(db_session):
    service = MessageService(db_session)
    data = MessageCreate(
        content="hello",
        sent_at=datetime.now(),
        chat_id=uuid4(),
        rating=1,
        role="user"
    )
    service.send_message(data, user_id=1)
    db_session.add.assert_called()
    db_session.commit.assert_called()
    db_session.refresh.assert_called()

def test_get_messages(db_session):
    service = MessageService(db_session)
    result = service.get_messages(user_id=1)
    assert isinstance(result, list)
    assert result[0].content == "test"

def test_update_message(db_session):
    service = MessageService(db_session)
    data = MessageCreate(
        content="updated",
        sent_at=datetime.now(),
        chat_id=uuid4(),
        rating=2,
        role="ai"
    )
    updated = service.update_message(message_id=uuid4(), message_data=data, user_id=1)
    assert updated.content == "updated"
    assert updated.rating == 2
    assert updated.role == "ai"
    db_session.commit.assert_called()
    db_session.refresh.assert_called()
