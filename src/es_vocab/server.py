from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import es_vocab.api.urls as urls
import es_vocab.db.cvs as cvs
import es_vocab.api.sparql as spq
from es_vocab.api import create_api_app



def initialization():
    cvs.init()
    urls.create_universe_term_routes()
    urls.create_project_term_routes()


def create_app() -> FastAPI:
    app = FastAPI()
    api_app = create_api_app()
    app.include_router(api_app.router)
    app.include_router(spq.sparql_router)
    app.mount("/", StaticFiles(directory="documentation/site", html=True), name="site")
    return app


def run_app(debug=False):
    initialization()
    import uvicorn

    uvicorn.run(
        create_app(),
        host="0.0.0.0",
        port=9999,
        proxy_headers=True,
        forwarded_allow_ips="*",
        reload=debug,
    )
