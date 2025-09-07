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
├── alembic.docker.ini
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

# Messages API Routes

This module defines the message-related endpoints of the application. It is built with **FastAPI**, uses **SQLAlchemy** for database access, and integrates **SlowAPI** for rate limiting.

---

## Key Features
- **Authentication required**: All routes depend on `get_current_user`, so only authenticated users can send, read, or update messages.  
- **Rate limiting**: Each endpoint has specific rate limits to prevent spam and abuse, implemented with `SlowAPI`.  
- **Service layer pattern**: Database operations are handled via the `MessageService` class, keeping routes clean and business logic separate.  


## Endpoints

 ### 1. Send a Message
 ```

POST /messages/

````
- **Rate limit**: `1/minute` per user  
- **Request body** (`MessageCreate`):
```json
{
  "recipient_id": "123",
  "content": "Hello, how are you?"
}
````

* **Response**:

```json
{
  "message": "Message sent successfully"
}
```

---

### 2. Get Messages

```
GET /messages/
```

* **Rate limit**: `10/minute` per user
* **Response** (list of `MessageRead`):

```json
[
  {
    "id": "a1b2c3",
    "sender_id": "123",
    "recipient_id": "456",
    "content": "Hello, how are you?",
    "timestamp": "2025-09-07T12:34:56"
  },
  {
    "id": "d4e5f6",
    "sender_id": "456",
    "recipient_id": "123",
    "content": "I’m good, thanks!",
    "timestamp": "2025-09-07T12:35:20"
  }
]
```

* **Errors**:

```json
{
  "detail": "No messages found"
}
```

---

### 3. Update a Message

```
PUT /messages/{message_id}
```

* **Rate limit**: `3/minute` per user
* **Path parameter**: `message_id` (string)
* **Request body** (`MessageBase`):

```json
{
  "content": "Updated message content"
}
```

* **Response** (`MessageBase`):

```json
{
  "id": "a1b2c3",
  "sender_id": "123",
  "recipient_id": "456",
  "content": "Updated message content",
  "timestamp": "2025-09-07T12:40:00"
}
```

* **Errors**:

```json
{
  "detail": "Message not found"
}
```

---

## Rate Limiting

The limiter uses a **per-user key function**:

* If authenticated → user ID is used.
* If not available → falls back to client IP.

This ensures fair usage and prevents abuse from both logged-in and anonymous clients.


# Authentication API Routes

This module defines the authentication-related endpoints of the application. It is built with **FastAPI**, uses **SQLAlchemy** for database access, and integrates a dedicated `AuthService` for handling registration, login, and token generation.

---

## Key Features
- **User registration**: Create a new user and receive an access token immediately after registering.  
- **User login**: Authenticate existing users and return a JWT access token.  
- **Service layer pattern**: Authentication logic is handled via `AuthService`.  
- **Error handling**: Returns standardized HTTP errors when validation fails or authentication is invalid.  

---

## Endpoints

### 1. Register
```

POST /auth/register

````
- **Request body** (`UserCreate`):
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "full_name": "Jane Doe"
}
````

* **Response** (`TokenSchema`):

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "token_type": "bearer"
}
```

* **Errors**:

```json
{
  "detail": "Email already registered"
}
```

---

### 2. Login

```
POST /auth/login
```

* **Request body** (`LoginSchema`):

```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

* **Response** (`TokenSchema`):

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "token_type": "bearer"
}
```

* **Errors**:

```json
{
  "detail": "Invalid credentials"
}
```

---

## Token Usage

The returned JWT `access_token` should be included in the `Authorization` header of subsequent requests:

```
Authorization: Bearer <access_token>
```

This ensures that protected routes can correctly identify and authorize the current user.

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
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql://your_db_user:your_db_password@localhost:5432/your_db_name
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
docker-compose exec app python -m alembic -c alembic.docker.ini upgrade head - running inside docker

python -m alembic -c alembic.ini upgrade head - running locally without docker
```

### API Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development
- Install dependencies: `pip install -r requirements.txt`
- Run locally: `PYTHONPATH=$(pwd) uvicorn src.app.main:app --reload`
- Run tests: `PYTHONPATH=$(pwd) pytest`

## Useful Commands
- View logs: `docker-compose logs app`
- Enter app container: `docker-compose exec app bash`
- Run Alembic migration: `alembic revision --autogenerate -m "message"`

### Known limitations
* CI/CD Pipeline could be implemented for things such as linting, deploying, running tests, etc
* Caching could be implemented using Redis
* Lack of monitoring (Prometheus, Grafana, Sentry, etc.)
* Custom exception handlers for things like DB errors could be implemented
