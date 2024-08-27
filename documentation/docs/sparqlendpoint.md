# SPARQL Endpoint


## What
The SPARQL endpoint offers a powerful query interface to access and manipulate vocabulary data using the SPARQL query language, specifically designed for querying RDF (Resource Description Framework) data.

## Why
The SPARQL endpoint enhances websemantic interoperability by enabling users to perform sophisticated and detailed queries on the vocabulary data. It also facilitates the seamless integration with other semantic web technologies and datasets, fostering a more interconnected and efficient data environment.

## How
To utilize the SPARQL endpoint, simply send your SPARQL queries to the provided endpoint URL. These queries can be used to retrieve, filter, and manipulate the vocabulary data according to your needs.

# YASGUI interface

you can find a yasgui interface : [https://es-vocab.ipsl.fr/sparql](http://es-vocab.ipsl.fr/sparql)

## Basic query

To get all triples in graph :

```http
SELECT *
WHERE {?s ?p ?o .}
```

## Institution query

```http

SELECT *
WHERE {?s <http://es-vocab.ipsl.fr/institution/acronyms> ?o .}
```
