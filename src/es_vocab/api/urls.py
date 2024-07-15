from collections.abc import Callable

from fastapi import APIRouter, HTTPException, status

import es_vocab.db.cvs as cvs

router = APIRouter()


def create_universe_term_end_point(datadescriptor_name: str) -> Callable:
    def _end_point(term_id: str):
        if term_id in cvs.TERMS_OF_UNIVERSE[datadescriptor_name]:
            return cvs.TERMS_OF_UNIVERSE[datadescriptor_name][term_id]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="term not found")

    return _end_point


def create_universe_term_routes():
    for datadescriptor_name, _ in cvs.TERMS_OF_UNIVERSE.items():
        router.add_api_route(
            f"/{datadescriptor_name}/{{term_id}}",
            endpoint=create_universe_term_end_point(datadescriptor_name),
            methods=["GET"],
        )


def create_project_term_end_point(project_name: str, collection_name: str) -> Callable:
    def _end_point(term_id: str):
        if term_id in cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS[project_name][collection_name]:
            return cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS[project_name][collection_name][term_id]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="term not found")

    return _end_point


def create_project_term_routes():
    for project_name, collection_contains in cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS.items():
        for collection_name, _ in collection_contains.items():
            router.add_api_route(
                f"/{project_name}/{collection_name}/{{term_id}}",
                endpoint=create_project_term_end_point(project_name, collection_name),
                methods=["GET"],
            )
