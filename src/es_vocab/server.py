import logging
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import es_vocab.api.sparql as spq
import es_vocab.api.urls as urls
import es_vocab.db.cvs as cvs
import es_vocab.utils.settings as settings
from es_vocab.api import create_api_app, webhook

_LOGGER = logging.getLogger("server")


def initialization():
    cvs.init()
    urls.create_universe_term_routes()
    urls.create_project_term_routes()


def create_app() -> FastAPI:
    app = FastAPI()
    api_app = create_api_app()
    app.include_router(api_app.router)
    app.include_router(spq.sparql_router)
    app.include_router(webhook.router)
    app.mount("/", StaticFiles(directory="documentation/site", html=True), name="site")
    return app


def run_app(debug=False):
    initialization()
    n_workers = (
        int(os.environ[settings.UVICORN_WORKERS_VAR_ENV_NAME])
        if settings.UVICORN_WORKERS_VAR_ENV_NAME in os.environ
        else 1
    )
    _LOGGER.info(f"number of uvicorn workers: {n_workers}")
    import uvicorn

    uvicorn.run(
        create_app(),
        host="0.0.0.0",
        port=settings.UVICORN_PORT,
        proxy_headers=True,
        forwarded_allow_ips="*",
        reload=debug,
        workers=n_workers,
    )
