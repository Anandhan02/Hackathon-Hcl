async def create_indexes(db):
    await db.users.create_index("email", unique=True)
