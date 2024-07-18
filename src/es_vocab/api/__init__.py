from fastapi import FastAPI

from . import db, urls

ROUTERS = [urls.router, db.router]


def create_api_app() -> FastAPI:
    api_app = FastAPI()
    for router in ROUTERS:
        api_app.include_router(router)
    return api_app
