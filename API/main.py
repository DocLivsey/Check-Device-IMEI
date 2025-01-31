from fastapi import FastAPI

from v1.api import create_app
from v1.routers.api import router

app = create_app(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
