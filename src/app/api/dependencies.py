import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request
from src.app.services.auth_service import verify_token as verify_jwt
from src.app.db.user import User 
from sqlalchemy.orm import sessionmaker


load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "15432")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)):
    authorization = request.headers.get("authorization")
    if not authorization:
        raise HTTPException(status_code=401, detail="Nedozvoljen pristup")
    try:
        token = authorization.split(" ")[1]
    except Exception:
        raise HTTPException(status_code=401, detail="Nedozvoljen pristup")
    payload = verify_jwt(token)
    user_id = payload.get("sub")
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Korisnik nije pronađen")
    return user
