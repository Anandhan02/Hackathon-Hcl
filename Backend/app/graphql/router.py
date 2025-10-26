from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema

# Create the GraphQL router with GraphiQL UI enabled
graphql_app = GraphQLRouter(schema, graphiql=True)
