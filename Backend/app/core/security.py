from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

# Setup bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    if password.startswith("$2b$") or password.startswith("$2a$"):
        # Already hashed (prevents double hashing existing users)
        return password
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(sub: str, extra: dict | None = None) -> str:
    """Create a signed JWT access token."""
    now = datetime.now(tz=timezone.utc)

    payload = {
        "sub": sub,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
    }

    if extra:
        payload.update(extra)

    encoded_jwt = jwt.encode(
        payload,                           #  correct variable
        settings.SECRET_KEY,               #  from .env
        algorithm=getattr(settings, "ALGORITHM", "HS256"),  #  safe default
    )

    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decode and validate JWT token."""
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,                       #  same key used in encoding
            algorithms=[getattr(settings, "ALGORITHM", "HS256")],
        )
    except JWTError:
        return {}
