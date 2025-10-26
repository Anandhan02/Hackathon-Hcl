from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId

class AccountIn(BaseModel):
    user_id: str
    account_type: str
    account_number: str
    balance: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AccountOut(BaseModel):
    id: str
    account_number: str
    account_type: str
    balance: float
    created_at: datetime
