import strawberry
from app.graphql.resolvers.user_resolver import MutationUser
from app.graphql.resolvers.account_resolver import MutationAccount, QueryAccount


@strawberry.type
class Query:
    status: str = "OK"

@strawberry.type
class Mutation(MutationUser, MutationAccount,QueryAccount):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
