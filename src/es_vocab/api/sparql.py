from rdflib_endpoint import SparqlRouter
from rdflib import Graph
import es_vocab.db.cvs as cvs

import es_vocab.utils.settings as settings

g = Graph()
g.parse(settings.GRAPH_PATH / "es-vocab.ttl")


sparql_router = SparqlRouter(
    graph=g,
    path="/sparql/",
    # Metadata used for the SPARQL service description and Swagger UI:
    title="SPARQL endpoint for es-vocab RDFLib graph ",
    description="A SPARQL endpoint to serve machine learning models, or any other logic implemented in Python. \n[Source code](https://github.com/vemonet/rdflib-endpoint)",
    version="0.1.0",
    public_url='http://es-vocab.ipsl.fr/',
)
