ES-VOCAB
========

Earth Science - VOCABulary

## How to contribute

### Python environment

```bash
pip install -e .
```

### Linters & code formatters

* If using pdm:

```bash
pdm install
pdm run pre-commit install
```
* Otherwise:

```bash
pip install pre-commit
pre-commit install
```

## Initial database population procedure

A pyessv archive must exist in `$HOME/.esdoc/pyessv-archive`, if it is not
present, run the following:

```shell
mkdir -p $HOME/.esdoc/pyessv-archive
git clone https://github.com/ES-DOC/pyessv-archive.git $HOME/.esdoc/pyessv-archive
```

### Using `pdm`:

```shell
pdm install
pdm run populate
```

### Without `pdm`:

```shell
pip install -e .
pip install 'dlt[duckdb]' pyessv pandas pyarrow
python -m es_vocab.db.fixtures.populate
python -m es_vocab.db.fixtures.after
```
