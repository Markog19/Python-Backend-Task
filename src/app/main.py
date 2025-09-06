from fastapi import FastAPI, HTTPException
from src.app.api.v1 import auth_router, messages_router
from slowapi.middleware import SlowAPIMiddleware
from src.app.core.exception_handlers import rate_limit_handler, http_exception_handler, generic_exception_handler
from slowapi.errors import RateLimitExceeded
from src.app.api.v1.messages_router import limiter


app = FastAPI(
    title="Python Messages Backend",
    description="Backend service for user authentication and message handling.",
    version="1.0.0",
)

# Add SlowAPI middleware
app.add_middleware(SlowAPIMiddleware)


app.openapi_schema = None

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = FastAPI.openapi(app)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.state.limiter = limiter

# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)


app.include_router(messages_router.router, prefix="/messages", tags=["messages"])
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)