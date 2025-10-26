import strawberry
from app.services.account_service import create_account,  get_account_by_email
from app.graphql.types.account_types import AccountType, CreateAccountInput

@strawberry.type
class MutationAccount:
    @strawberry.mutation
    async def createAccount(self, info, input: CreateAccountInput) -> AccountType:
        # Simulate authenticated user for now (replace later with JWT context)
        user_id = "mocked_user_id"

        try:
            result = await create_account(
                user_id=user_id,
                account_type=input.accountType.lower(),
                initial_deposit=input.initialDeposit
            )
            return AccountType(
                id=result.id,
                accountNumber=result.account_number,
                accountType=result.account_type,
                balance=result.balance,
                createdAt=result.created_at
            )
        except ValueError as e:
            raise Exception(str(e))

@strawberry.type
class QueryAccount:
    @strawberry.field
    async def getAccountByEmail(self, email: str) -> AccountType:
        try:
            account = await get_account_by_email(email)
            return AccountType(
                id=account.id,
                accountNumber=account.account_number,
                accountType=account.account_type,
                balance=account.balance,
                createdAt=account.created_at
            )
        except ValueError as e:
            raise Exception(str(e))

