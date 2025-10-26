import uvicorn
from fastapi import FastAPI
from app.core.config import settings
from app.core.cors import apply_cors
from app.db.mongo import connect_to_mongo, close_mongo_connection
from app.graphql.router import graphql_app  # import directly here
from app.core.middleware import JWTBlacklistMiddleware


app = FastAPI(title=settings.APP_NAME)
apply_cors(app)
app.add_middleware(JWTBlacklistMiddleware)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "Welcome to SmartBank API! Visit /graphql for the GraphQL endpoint."}

#  Mount GraphQL directly under /graphql
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
