import strawberry
from fastapi import Header
from app.services.auth_service import blacklist_token
from app.graphql.types.user_types import UserType

@strawberry.type
class MutationAuth:
    @strawberry.mutation
    async def logoutUser(self, info, authorization: str = Header(None)) -> bool:
        """Invalidate token by blacklisting it."""
        if not authorization:
            return False
        token = authorization.replace("Bearer ", "")
        await blacklist_token(token)
        return True
