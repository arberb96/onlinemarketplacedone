from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .db import models
from .db.database import engine
from .routers import users, posts, auth, categories, products, carts

import sys
sys.path.append(".")


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="DBMS Project api",
    description="Simple online marketplace api",
    version="0.1.0",
)

#Include routers
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(carts.router)

#Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/healthcheck")
async def root():
    return {"message": "Hello World!"}

"uvicorn app.main:app --reload"
