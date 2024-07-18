from fastapi import APIRouter, HTTPException, status

import es_vocab.db.cvs as cvs

router = APIRouter(prefix="/api")

# TODO: support case sensitive and not ???

# TODO:
# Return the path at the same time:
# @router.get('/universe/term/{term_id}') # Return the dictionary of the terms that match the specified term id within the universe.
# @router.get('/project/term/{term_id}') # Return the dictionary of the terms that match the specified term id within all projects.
# @router.get('/term/{term_id}') # Return the dictionary of the terms that match the specified term id within the universe and all projects.
# @router.get('/collection/{collection_name}') # Return the dictionary of the collection names that match the specified collection name within all projects.


# Return the list of the data descriptor names.
@router.get("/universe/datadescriptor")
async def get_all_data_descriptor_names() -> list:
    return list(cvs.TERMS_OF_UNIVERSE.keys())


def _get_all_term_from_data_descriptor(data_descriptor_name: str) -> list:
    if term_specs := cvs.TERMS_OF_UNIVERSE.get(data_descriptor_name, None):
        return term_specs
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"data descriptor {data_descriptor_name} not found"
        )


# Check a data descriptor.
@router.get("/universe/datadescriptor/{data_descriptor_name}")
def check_data_descriptor_name(data_descriptor_name: str):
    _get_all_term_from_data_descriptor(data_descriptor_name)


# Return the list of the terms in the specified data descriptor.
@router.get("/universe/datadescriptor/{data_descriptor_name}/term")
async def get_all_term_from_data_descriptor(data_descriptor_name: str) -> list:
    return list(_get_all_term_from_data_descriptor(data_descriptor_name).values())


# Return the term that matches the specified term id within the specified data descriptor.
@router.get("/universe/datadescriptor/{data_descriptor_name}/term/{term_id}")
async def get_term_by_id_from_data_descriptor(data_descriptor_name: str, term_id: str):
    term_specs = _get_all_term_from_data_descriptor(data_descriptor_name)
    if term := term_specs.get(term_id, None):
        return term
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"term {term_id} not found in data descriptor {data_descriptor_name}",
        )


# Return the list of the project names.
@router.get("/project")
async def get_all_project_names() -> list:
    return list(cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS.keys())


def _get_collections(project_name: str):
    if collections := cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS.get(project_name, None):
        return collections
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"project {project_name} not found")


def _get_collection(project_name: str, collection_name: str):
    collections = _get_collections(project_name)
    if collection := collections.get(collection_name, None):
        return collection
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"collection {collection_name} not found in project {project_name}",
        )


# TODO: to be replaced be the project specs.
@router.get("/project/{project_name}")
async def check_project_name(project_name: str):
    if project_name not in cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"project {project_name} not found")


# Return the list of the collection names in the specified project.
@router.get("/project/{project_name}/collection")
async def get_all_collections_from_project(project_name: str) -> list:
    return list(_get_collections(project_name).keys())


@router.get("/project/{project_name}/collection/{collection_name}")
async def check_collection_name(project_name: str, collection_name: str):
    _get_collection(project_name, collection_name)


# Return the list of the terms in the specified collection within the specified project.
@router.get("/project/{project_name}/collection/{collection_name}/term")
async def get_terms_from_collection(project_name: str, collection_name: str):
    collection = _get_collection(project_name, collection_name)
    return list(collection.keys())


# Return the term that matches the specified term id in the specified collection within the specified project.
@router.get("/project/{project_name}/collection/{collection_name}/term/{term_id}")
async def get_term_from_collection(project_name: str, collection_name: str, term_id: str):
    collection = _get_collection(project_name, collection_name)
    if term := collection.get(term_id, None):
        return term
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"term {term_id} not found in collection {collection_name} from project {project_name}",
        )
