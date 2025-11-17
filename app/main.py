from fastapi import FastAPI
from .db import connect_to_mongo, close_mongo_connection
from .routers import books, users, loans

app = FastAPI(title="Library Management System")


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(loans.router, prefix="/loans", tags=["loans"])
