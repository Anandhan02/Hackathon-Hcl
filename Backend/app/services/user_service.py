from datetime import datetime, timezone
from bson import ObjectId
from pydantic import EmailStr
from app.db.mongo import get_db
from app.models.user import UserIn, UserOut, AuthPayload
from app.core.security import hash_password, create_access_token, verify_password


async def register_user(user: UserIn) -> AuthPayload:
    #  Always get the active MongoDB connection
    db = get_db()
    users = db.users

    email = user.email.lower()
    print("DB in register_user:", db)

    #  Check if user already exists
    existing = await users.find_one({"email": email})
    if existing:
        raise ValueError("Email already registered")

    #  Prepare user document
    user_doc = {
        "name": user.name,
        "email": email,
        "password_hash": hash_password(user.password),
        "roles": ["CUSTOMER"],
        "created_at": datetime.now(timezone.utc),
    }

    #  Insert into database
    result = await users.insert_one(user_doc)
    uid = str(result.inserted_id)

    #  Generate JWT token
    token = create_access_token({"sub": uid, "roles": user_doc["roles"]})

    #  Prepare response payload
    user_out = UserOut(id=uid, name=user.name, email=email, roles=user_doc["roles"])
    return AuthPayload(accessToken=token, user=user_out)


async def login_user(email: str, password: str) -> AuthPayload:
    db = get_db()
    users = db.users

    # Normalize email
    email = email.lower()
    user = await users.find_one({"email": email})

    if not user:
        raise ValueError("Invalid email or password")

    # Verify password
    if not verify_password(password, user["password_hash"]):
        raise ValueError("Invalid email or password")

    # Create JWT
    token_data = {"sub": str(user["_id"]), "roles": user.get("roles", ["CUSTOMER"])}
    access_token = create_access_token(token_data)

    # Return structured response
    user_out = UserOut(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        roles=user.get("roles", ["CUSTOMER"])
    )

    return AuthPayload(accessToken=access_token, user=user_out)
