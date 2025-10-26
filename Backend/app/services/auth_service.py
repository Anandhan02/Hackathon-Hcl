from datetime import datetime, timezone
from jose import jwt, JWTError
from app.db.mongo import get_db
from app.core.config import get_settings

settings = get_settings()
db=get_db

async def blacklist_token(token: str):
    """Add token to blacklist collection."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        exp = payload.get("exp")
        user_id = payload.get("sub")
        doc = {
            "token": token,
            "user_id": user_id,
            "exp": exp,
            "created_at": datetime.now(timezone.utc),
        }
        await db().blacklist_tokens.insert_one(doc)
    except JWTError:
        # Invalid or already expired token
        pass

async def is_token_blacklisted(token: str) -> bool:
    """Check if token is in blacklist."""
    existing = await db().blacklist_tokens.find_one({"token": token})
    return existing is not None
