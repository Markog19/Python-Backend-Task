import os
from sqlalchemy.orm import Session
from src.app.db.user import User
from src.app.schemas.auth_schema import RegisterSchema, LoginSchema
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from src.app.core.logging import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")  # Change to env var in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class AuthService:
    jwt_blacklist = set()

    @staticmethod
    def register(user: RegisterSchema, db: Session):
        print("test")
        existing = db.query(User).filter(
            User.email == user.email
        ).first()
        if existing:
            return None
        hashed_lozinka = pwd_context.hash(user.lozinka)
        db_user = User(
            ime=user.ime,
            prezime=user.prezime,
            email=user.email,
            hashed_password=hashed_lozinka
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
        if not db_user or not pwd_context.verify(user.lozinka, db_user.hashed_lozinka):
            return None
        access_token = AuthService.create_access_token({"sub": str(db_user.id)})
        return {"user": db_user, "access_token": access_token}

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire, "iat": datetime.now()})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            return user_id
        except jwt.PyJWTError:
            return None