# app/core/middleware.py

from fastapi import Request
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.config import settings
from app.services.auth_service import is_token_blacklisted


class JWTBlacklistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                if await is_token_blacklisted(token):
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Token blacklisted"},
                    )
            except JWTError:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid or expired token"},
                )

        # Continue request if everything is okay
        return await call_next(request)
