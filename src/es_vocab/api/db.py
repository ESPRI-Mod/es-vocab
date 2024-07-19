from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

import es_vocab.db.cvs as cvs

router = APIRouter(prefix="/api")

# TODO: support case sensitive and not ???


# Return the list of the data descriptor names.
@router.get("/universe/datadescriptor")
async def get_all_data_descriptor_ids() -> list:
    return list(cvs.TERMS_OF_UNIVERSE.keys())


def _get_all_term_from_data_descriptor(data_descriptor_id: str) -> list:
    if term_specs := cvs.TERMS_OF_UNIVERSE.get(data_descriptor_id, None):
        return term_specs
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"data descriptor {data_descriptor_id} not found"
        )


# Check a data descriptor.
@router.get("/universe/datadescriptor/{data_descriptor_id}")
def check_data_descriptor_id(data_descriptor_id: str):
    _get_all_term_from_data_descriptor(data_descriptor_id)


# Return the list of the terms in the specified data descriptor.
@router.get("/universe/datadescriptor/{data_descriptor_id}/term")
async def get_all_term_from_data_descriptor(data_descriptor_id: str) -> list:
    return list(_get_all_term_from_data_descriptor(data_descriptor_id).values())


# Return the term that matches the specified term id within the specified data descriptor.
@router.get("/universe/datadescriptor/{data_descriptor_id}/term/{term_id}")
async def get_term_by_id_from_data_descriptor(data_descriptor_id: str, term_id: str):
    term_specs = _get_all_term_from_data_descriptor(data_descriptor_id)
    if term := term_specs.get(term_id, None):
        return term
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"term {term_id} not found in data descriptor {data_descriptor_id}",
        )


# Return the list of the project names.
@router.get("/project")
async def get_all_project_ids() -> list:
    return list(cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS.keys())


def _get_collections(project_id: str):
    if collections := cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS.get(project_id, None):
        return collections
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"project {project_id} not found")


def _get_collection(project_id: str, collection_id: str):
    collections = _get_collections(project_id)
    if collection := collections.get(collection_id, None):
        return collection
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"collection {collection_id} not found in project {project_id}",
        )


# TODO: to be replaced be the project specs.
@router.get("/project/{project_id}")
async def check_project_id(project_id: str):
    if project_id not in cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"project {project_id} not found")


# Return the list of the collection names in the specified project.
@router.get("/project/{project_id}/collection")
async def get_all_collections_from_project(project_id: str) -> list:
    return list(_get_collections(project_id).keys())


@router.get("/project/{project_id}/collection/{collection_id}")
async def check_collection_id(project_id: str, collection_id: str):
    _get_collection(project_id, collection_id)


# Return the list of the terms in the specified collection within the specified project.
@router.get("/project/{project_id}/collection/{collection_id}/term")
async def get_terms_from_collection(project_id: str, collection_id: str):
    collection = _get_collection(project_id, collection_id)
    return list(collection.keys())


# Return the term that matches the specified term id in the specified collection within the specified project.
@router.get("/project/{project_id}/collection/{collection_id}/term/{term_id}")
async def get_term_from_collection(project_id: str, collection_id: str, term_id: str):
    collection = _get_collection(project_id, collection_id)
    if term := collection.get(term_id, None):
        return term
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"term {term_id} not found in collection {collection_id} from project {project_id}",
        )


def _format_general_item_search(term: BaseModel, path: str, item_name: str) -> dict:
    return {item_name: term, "path": path}


def _search_term_in_universe(term_id: str) -> list[dict]:
    result = list()
    for data_descriptor_id, terms in cvs.TERMS_OF_UNIVERSE.items():
        if term_id in terms:
            result.append(
                _format_general_item_search(
                    terms[term_id], f"/universe/datadescriptor/{data_descriptor_id}/term/{term_id}", "term"
                )
            )
    return result


def _search_term_in_all_projects(term_id: str) -> list[dict]:
    result = list()
    for project_id, collections in cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS.items():
        for collection_id, collection in collections.items():
            if term_id in collection:
                result.append(
                    _format_general_item_search(
                        collection[term_id],
                        f"/project/{project_id}/collection/{collection_id}/term/{term_id}",
                        "term",
                    )
                )
    return result


# Return the terms that match the specified term id within the universe.
@router.get("/universe/term/{term_id}")
async def search_term_in_universe(term_id: str) -> list[dict]:
    result = _search_term_in_universe(term_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"term {term_id} not found in universe")
    return result


# Return the terms that match the specified term id within all the projects.
@router.get("/project/term/{term_id}")
async def search_term_in_all_projects(term_id: str) -> list[dict]:
    result = _search_term_in_all_projects(term_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"term {term_id} not found accross the projects"
        )
    return result


# Return the terms that match the specified term id within the universe and all projects.
@router.get("/term/{term_id}")
async def search_term_in_universe_and_all_projects(term_id: str) -> list[dict]:
    result = _search_term_in_universe(term_id)
    result.extend(_search_term_in_all_projects(term_id))
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"term {term_id} not found accross the universe and the projects",
        )
    return result


# Return the collection names that match the specified collection name within all projects.
@router.get("/collection/{collection_id}")
async def search_collection_in_all_projects(collection_id: str) -> list[dict]:
    result = list()
    for project_id, collections in cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS.items():
        if collection_id in collections:
            result.append(
                _format_general_item_search(
                    collection_id, f"/project/{project_id}/collection/{collection_id}", "collection_id"
                )
            )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"collection {collection_id} not found accross the projects"
        )
    return result
