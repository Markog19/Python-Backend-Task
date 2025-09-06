from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from src.app.core.logging import logger

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
