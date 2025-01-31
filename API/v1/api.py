from fastapi import FastAPI, APIRouter
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from typing import List


def init_routers(app_: FastAPI, router: APIRouter) -> None:
    app_.include_router(router)


origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
]


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]
    return middleware
