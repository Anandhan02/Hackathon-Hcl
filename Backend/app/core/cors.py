from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.core.config import settings

def apply_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
