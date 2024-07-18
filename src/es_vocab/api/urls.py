from collections.abc import Callable
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

import es_vocab.db.cvs as cvs

router = APIRouter()


def to_str(value: any) -> str:
    result = ""
    if isinstance(value, list):
        match len(value):
            case 0:
                pass
            case 1:
                result = to_str(value[0])
            case _:
                result = str(value)
    elif isinstance(value, dict):
        return str(value)
    else:
        result = str(value)
    return result


def from_json_to_html(json_obj: BaseModel) -> str:
    result = "<!DOCTYPE html>\n<html>\n<body>\n<ul>\n"
    for key, value in json_obj.model_dump().items():
        result += f"<li>{key}: {to_str(value)}</li>\n"
    result += "</ul>\n</body>\n</html>"
    return result


def format_term(term: BaseModel, accept_type: str) -> JSONResponse | HTMLResponse:
    if "application/json" in accept_type:
        return JSONResponse(term.model_dump_json())
    else:
        return HTMLResponse(from_json_to_html(term))


def create_universe_term_end_point(datadescriptor_name: str) -> Callable:
    def _end_point(term_id: str, accept: Annotated[str | None, Header()]):
        if term_id in cvs.TERMS_OF_UNIVERSE[datadescriptor_name]:
            return format_term(cvs.TERMS_OF_UNIVERSE[datadescriptor_name][term_id], accept)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="term not found")

    return _end_point


def create_universe_term_routes():
    for datadescriptor_name, _ in cvs.TERMS_OF_UNIVERSE.items():
        router.add_api_route(
            path=f"/{datadescriptor_name}/{{term_id}}",
            endpoint=create_universe_term_end_point(datadescriptor_name),
            response_model=cvs.DATA_DESCRIPTOR_CLASS[datadescriptor_name],
            methods=["GET"],
        )


def create_project_term_end_point(project_name: str, collection_name: str) -> Callable:
    def _end_point(term_id: str, accept: Annotated[str | None, Header()]):
        if term_id in cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS[project_name][collection_name]:
            return format_term(cvs.TERMS_OF_COLLECTIONS_OF_PROJECTS[project_name][collection_name][term_id], accept)
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
