# Message Service

A FastAPI-based backend service for sending, updating, and retrieving messages, with JWT authentication and PostgreSQL database support. The project is fully containerized using Docker and Docker Compose.

## Features
- User registration and authentication (JWT)
- Send, update, and retrieve messages
- PostgreSQL database with Alembic migrations
- Centralized logging and exception handling
- LRU caching examples
- Dockerized app and database

## Project Structure
```
message-service/
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
├── requirements.txt
├── .env
├── .gitignore
├── migrations/
│   └── versions/
├── src/
│   └── app/
│       ├── main.py
│       ├── api/
│       │   └── v1/
│       │       └── messages_router.py
│       ├── core/
│       │   ├── config.py
│       │   ├── logging.py
│       │   └── exception_handlers.py
│       ├── db/
│       │   ├── base.py
│       │   ├── message.py
│       │   └── user.py
│       ├── schemas/
│       │   ├── messages.py
│       │   └── user.py
│       └── services/
│           ├── message_service.py
│           └── auth_service.py
└── tests/
```

## Getting Started

### Prerequisites
- Docker & Docker Compose
- (Optional) Python 3.12+ for local development

### Environment Variables
Copy `.env` and adjust as needed:
```
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://your_db_user:your_db_password@db:5432/your_db_name
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Build and Run with Docker Compose
```bash
docker-compose up --build
```
- App: http://localhost:8000
- DB:  localhost:15432 (for external tools like DBeaver)

### Run Migrations
```bash
docker-compose exec app alembic upgrade head
```

### API Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development
- Install dependencies: `pip install -r requirements.txt`
- Run locally: `uvicorn src.app.main:app --reload`
- Run tests: `pytest`

## Useful Commands
- View logs: `docker-compose logs app`
- Enter app container: `docker-compose exec app bash`
- Run Alembic migration: `alembic revision --autogenerate -m "message"`

## License
MIT
