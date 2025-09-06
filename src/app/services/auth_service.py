import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from src.app.db.user import User
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from src.app.core.logging import logger
from src.app.schemas.user import LoginSchema, UserCreate
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")  # Change to env var in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class AuthService:

    @staticmethod
    def register(user:UserCreate , db: Session):
        print("test")
        existing = db.query(User).filter(
            User.email == user.email
        ).first()
        if existing:
            return None
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def login(user: LoginSchema, db: Session):
        db_user = db.query(User).filter(
            User.email == user.email
        ).first()
        if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
            return None
        access_token = AuthService.create_access_token({"sub": str(db_user.id)})
        return access_token

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire, "iat": datetime.now()})
        encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
        return encoded_jwt

    

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            return user_id
        except jwt.PyJWTError:
            return None