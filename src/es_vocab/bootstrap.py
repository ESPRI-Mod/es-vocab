import logging
import os

import es_vocab.utils.settings as settings

_LOGGER = logging.getLogger("server")


def run_app():
    n_workers = (
        int(os.environ[settings.UVICORN_WORKERS_VAR_ENV_NAME])
        if settings.UVICORN_WORKERS_VAR_ENV_NAME in os.environ
        else 1
    )
    _LOGGER.info(f"number of uvicorn workers: {n_workers}")
    import uvicorn

    uvicorn.run(
        app="src.es_vocab.server:app",
        host="0.0.0.0",
        port=settings.UVICORN_PORT,
        proxy_headers=True,
        forwarded_allow_ips="*",
        reload=False,
        workers=n_workers,
    )
