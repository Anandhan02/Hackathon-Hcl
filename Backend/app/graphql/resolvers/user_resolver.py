import strawberry
from app.models.user import UserIn
from app.services.user_service import register_user, login_user
from app.graphql.types.user_types import RegisterInput, AuthPayloadType, UserType, LoginInput


@strawberry.type
class MutationUser:
    @strawberry.mutation
    async def registerUser(self, input: RegisterInput) -> AuthPayloadType:
        """
        Register a new user and return an access token + user info.
        """
        try:
            user_in = UserIn(
                name=input.name,
                email=input.email,
                password=input.password,
            )

            result = await register_user(user_in)

            return AuthPayloadType(
                accessToken=result.accessToken,
                user=UserType(
                    id=result.user.id,
                    name=result.user.name,
                    email=result.user.email,
                    roles=result.user.roles,
                ),
            )

        except ValueError as e:
            raise Exception(str(e))
        except Exception as e:
            raise Exception(f"Registration failed: {e}")

    @strawberry.mutation
    async def loginUser(self, input: LoginInput) -> AuthPayloadType:
        """
        Log in an existing user and return an access token + user info.
        """
        try:
            result = await login_user(input.email, input.password)

            return AuthPayloadType(
                accessToken=result.accessToken,
                user=UserType(
                    id=result.user.id,
                    name=result.user.name,
                    email=result.user.email,
                    roles=result.user.roles,
                ),
            )

        except ValueError as e:
            raise Exception(str(e))
        except Exception as e:
            raise Exception(f"Login failed: {e}")
