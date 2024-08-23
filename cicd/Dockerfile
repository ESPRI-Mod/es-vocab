FROM python:3.12.3-alpine3.20 AS es-vocab

RUN apk update && apk upgrade

WORKDIR /var/www
ADD https://github.com/ESPRI-Mod/es-vocab.git#main es-vocab
ADD https://github.com/ESPRI-Mod/WGCM_CVs.git#main  WGCM_CVs

WORKDIR /var/www/projects
ADD https://github.com/ESPRI-Mod/CMIP6Plus_CVs.git#main projects/CMIP6Plus_CVs

WORKDIR /var/www/es-vocab
RUN pip install .

CMD ["python","-c","from es_vocab.server import run_app; run_app()"]
