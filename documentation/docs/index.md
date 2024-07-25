# es-vocab Documentation

Welcome to the es-vocab documentation. This documentation provides a comprehensive guide on what es-vocab is, why it is essential, and how to use it effectively.

## Overview

**es-vocab** is a controlled vocabulary service designed to manage and serve standardized terms and metadata for various projects. It ensures consistency and interoperability across different systems and users by providing access to a centralized repository of terms and associated metadata.

The service is structured around three main components:

1. **WGCM_CVs Repository**: The main repository that inventories all possible values of terms along with their metadata.
2. **Project-Specific Repositories**: Each project (e.g., CMIP6Plus) has its own repository where collections of IDs from the WGCM_CVs repository are listed, with the possibility to add or change metadata as necessary.
3. **Service Interfaces**: es-vocab serves vocabulary to different users via a REST API, a website, and a SPARQL endpoint for web semantic interoperability.

## What is es-vocab?

**es-vocab** is a service that manages controlled vocabularies, which are standardized sets of terms and their definitions. These vocabularies are crucial for ensuring that different systems and users refer to the same concepts in a consistent manner. 

### Components

1. **WGCM_CVs Repository**:
   **Data-Descriptor Categories**: Inventory of all possible term values and associated metadata.

2. **Project-Specific Repositories**:
   **Collections**: Lists of IDs from the WGCM_CVs repository specific to each project, with potential additional or modified metadata.

3. **Service Interfaces**:
    1. **REST API** : For programmatic access. details [here](restapi.md)   
    2. **Website**: For human users. more details [here](website.md)
    3. **SPARQL Endpoint**: For web semantic interoperability, with IRIs pointing to the website. more details [here](sparqlendpoint.md)


## Why use es-vocab?

Controlled vocabularies are essential for several reasons:

1. **Consistency**: Ensures that all users and systems use the same terms in the same way.
2. **Interoperability**: Facilitates communication and data exchange between different systems and projects.
3. **Efficiency**: Reduces the need for rework and clarifications by providing a single source of truth for terms and their definitions.
4. **Quality Control**: Helps maintain high data quality by enforcing standardized term usage.

