import logging
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import es_vocab.api.sparql as spq
import es_vocab.api.urls as urls
import es_vocab.db.cvs as cvs
from es_vocab.api import create_api_app, webhook

_LOGGER = logging.getLogger("server")


def initialization():
    _LOGGER.info(f"initialization of process {os.getpid()}")
    cvs.init()
    urls.create_universe_term_routes()
    urls.create_project_term_routes()
    
    # DEBUG
    from sqlalchemy.ext.asyncio import create_async_engine
    db_url = 'sqlite+aiosqlite:///db.sqlite'
    engine = create_async_engine(db_url, echo=False)
    print(f"engine for {os.getpid()}: {engine}")


def create_app() -> FastAPI:
    app = FastAPI()
    api_app = create_api_app()
    app.include_router(api_app.router)
    app.include_router(spq.sparql_router)
    app.include_router(webhook.router)
    #app.mount("/", StaticFiles(directory="documentation/site", html=True), name="site") # not needed anymore serve on github.io (https://espri-mod.github.io/es-vocab/website/)
    return app


initialization()
app = create_app()
