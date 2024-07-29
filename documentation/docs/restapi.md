# REST API

The REST API is a core component of the es-vocab service, providing programmatic access to the controlled vocabularies. It allows users to retrieve term definitions and associated metadata efficiently.

## What is the REST API?

The REST API of es-vocab is an interface designed for programmatic access to the controlled vocabularies. It leverages the FastAPI framework to deliver a robust and high-performance API with automatically generated documentation.

## Why use the REST API?

Using the REST API provides several benefits:

1. **Automation**: Enables automated systems and applications to access vocabulary terms and metadata without manual intervention.
2. **Efficiency**: Provides quick and consistent access to standardized terms, improving data processing and integration workflows.
3. **Interoperability**: Facilitates seamless communication between different systems and services by using a common vocabulary.
4. **Scalability**: Supports large-scale data access and manipulation, essential for big data applications and services.

## How to use the REST API?

The REST API is hosted at [http://es-vocab.ipsl.fr](http://es-vocab.ipsl.fr). Below are some common usage examples and endpoints.

### Endpoints
#### Swagger api documentation 

[http://es-vocab.ipsl.fr/docs](http://es-vocab.ipsl.fr/docs)

#### Retrieve institution Term Metadata

```http
curl -X 'GET' \
  'http://es-vocab.ipsl.fr/api/universe/datadescriptor/institution/term' \
  -H 'accept: application/json'
```
