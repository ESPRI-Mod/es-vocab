from rdflib import Graph
from rdflib_endpoint import SparqlRouter

import es_vocab.utils.settings as settings

SPARQL_ROOT_PATH = "/sparql"

g = Graph()
g.parse(settings.GRAPH_DIR_PATH / "es-vocab.ttl")


sparql_router = SparqlRouter(
    graph=g,
    path=SPARQL_ROOT_PATH,
    # Metadata used for the SPARQL service description and Swagger UI:
    title="SPARQL endpoint for es-vocab RDFLib graph",
    description="A SPARQL endpoint to serve machine learning models, or any other logic implemented in Python. \n[Source code](https://github.com/vemonet/rdflib-endpoint)",
    version="0.1.0",
    public_url=f"http://{settings.API_SERVER_DOMAINE_NAME}{SPARQL_ROOT_PATH}",
)
