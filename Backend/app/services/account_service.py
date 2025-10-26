import random
from datetime import datetime
from app.db.mongo import get_db
from app.models.account_model import AccountIn, AccountOut

VALID_ACCOUNT_TYPES = ["savings", "current", "fixed_deposit"]

# Minimum deposits per type
MIN_DEPOSITS = {
    "savings": 1000.0,
    "current": 2000.0,
    "fixed_deposit": 5000.0
}


def generate_account_number() -> str:
    """Generate a random 10-digit account number"""
    return str(random.randint(10**9, (10**10) - 1))


async def create_account(user_id: str, account_type: str, initial_deposit: float) -> AccountOut:
    if account_type not in VALID_ACCOUNT_TYPES:
        raise ValueError("Invalid account type. Must be savings, current, or fixed_deposit.")

    min_required = MIN_DEPOSITS[account_type]
    if initial_deposit < min_required:
        raise ValueError(f"Minimum deposit for {account_type} is {min_required}.")

    db = get_db()
    accounts = db.accounts

    account_number = generate_account_number()

    account_doc = {
        "user_id": user_id,
        "account_type": account_type,
        "account_number": account_number,
        "balance": initial_deposit,
        "created_at": datetime.utcnow(),
    }

    result = await accounts.insert_one(account_doc)
    return AccountOut(
        id=str(result.inserted_id),
        account_number=account_number,
        account_type=account_type,
        balance=initial_deposit,
        created_at=account_doc["created_at"]
    )




async def get_account_by_email(email: str) -> AccountOut | None:
    db = get_db()
    users = db.users
    accounts = db.accounts

    # find the user first
    user = await users.find_one({"email": email.lower()})
    if not user:
        raise ValueError("User not found.")

    # find the account belonging to this user
    account = await accounts.find_one({"user_id": str(user["_id"])})
    if not account:
        raise ValueError("No account found for this user.")

    return AccountOut(
        id=str(account["_id"]),
        account_number=account["account_number"],
        account_type=account["account_type"],
        balance=account["balance"],
        created_at=account["created_at"],
    )