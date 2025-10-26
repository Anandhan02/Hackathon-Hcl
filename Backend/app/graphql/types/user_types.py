import strawberry
from typing import List



@strawberry.type
class UserType:
    id: strawberry.ID
    name: str
    email: str
    roles: List[str]


@strawberry.type
class AuthPayloadType:
    accessToken: str
    user: UserType



@strawberry.input
class RegisterInput:
    name: str
    email: str
    password: str


@strawberry.input
class LoginInput:
    email: str
    password: str
