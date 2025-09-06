from fastapi import FastAPI, Request, HTTPException
from src.app.api.v1 import auth_router, messages_router
from src.app.core.logging import logger
from src.app.core.exception_handlers import http_exception_handler, generic_exception_handler

app = FastAPI(
    title="Python Messages Backend",
    description="Backend service for user authentication and message handling.",
    version="1.0.0",
)


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
# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(messages_router.router, prefix="/messages", tags=["messages"])
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)