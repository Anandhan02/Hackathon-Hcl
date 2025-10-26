import strawberry
from datetime import datetime

@strawberry.type
class AccountType:
    id: strawberry.ID
    accountNumber: str
    accountType: str
    balance: float
    createdAt: datetime

@strawberry.input
class CreateAccountInput:
    accountType: str
    initialDeposit: float
