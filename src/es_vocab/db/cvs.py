import importlib.util
import inspect
import json
import logging
from pathlib import Path

from pydantic import BaseModel

import es_vocab.utils.settings as settings

_LOGGER = logging.getLogger("cvs")


def check_data_descriptor(data_descriptor_name: str) -> bool:
    return data_descriptor_name in TERMS_OF_UNIVERSE


def get_term(data_descriptor_name: str, term_id: str) -> BaseModel | None:
    if terms_of_data_descriptor := TERMS_OF_UNIVERSE.get(data_descriptor_name, None):
        return terms_of_data_descriptor.get(term_id, None)
    else:
        return None


def _get_classes_from_module(module) -> dict[str, type]:
    # inspect.getmembers gets all classes defined in the module.
    classes = inspect.getmembers(module, inspect.isclass)
    # Filter out classes that are not defined in this module
    module_classes = {name: cls for name, cls in classes if cls.__module__ == module.__name__}
    return module_classes


def _load_pydantic_class(pydantic_module_file_path: Path) -> type:
    class_name = settings.from_pydantic_module_filepath_to_pydantic_class_name(pydantic_module_file_path)
    try:
        spec = importlib.util.spec_from_file_location(name=class_name, location=pydantic_module_file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        classes = _get_classes_from_module(module)
        result = classes[class_name]
        return result
    except FileNotFoundError:
        _LOGGER.error(f"file {pydantic_module_file_path} not found")
    except KeyError:
        _LOGGER.error(f"class {class_name} not found in {pydantic_module_file_path}")


def _parse_terms_of_universe(universe_dir_path: Path) -> dict[str, dict[str, BaseModel]]:
    result = dict()
    for data_descriptor_dir_path in universe_dir_path.iterdir():
        _LOGGER.debug(f"parse dir {data_descriptor_dir_path}")
        result[data_descriptor_dir_path.name] = dict()
        pydantic_class_module_file_path = settings.compute_pydantic_file_path_from_data_descriptor_dir_path(
            data_descriptor_dir_path
        )
        pydantic_class = _load_pydantic_class(pydantic_class_module_file_path)
        _LOGGER.debug(f"found pydantic class: {pydantic_class}")
        for term_file_path in data_descriptor_dir_path.glob("**/*.json"):
            _LOGGER.debug(f"parse file {term_file_path}")
            try:
                json_content_file = Path(term_file_path).read_text()
                pydantic_instance = pydantic_class.model_validate_json(json_content_file)
                result[data_descriptor_dir_path.name][pydantic_instance.id] = pydantic_instance
            except Exception as e:
                _LOGGER.error(f"unable to parse {term_file_path}:\n{str(e)}")
    return result


def _parse_collections_of_project(project_dir_path: Path) -> dict[str : dict[str:BaseModel]]:
    result = dict()
    for collection_file_path in project_dir_path.glob("*.json"):
        _LOGGER.debug(f"parse collection: {collection_file_path}")
        collection_name = settings.from_collection_file_path_to_collection_name(collection_file_path)
        result[collection_name] = dict()
        collection_content = json.loads(collection_file_path.read_text())
        for term_specs_from_collection in collection_content[settings.COLLECTION_TERM_SPECS_LIST_NODE_NAME]:
            term_id = term_specs_from_collection.pop(settings.ID_NODE_NAME)
            data_descriptor_name = term_specs_from_collection.pop(settings.TYPE_NODE_NAME)
            if not check_data_descriptor(data_descriptor_name):
                _LOGGER.error(f"can't find data descriptor {data_descriptor_name}")
                break
            term_from_universe = get_term(data_descriptor_name, term_id)
            if term_from_universe is None:
                _LOGGER.error(f"can't find term {term_id} in data descriptor {data_descriptor_name}")
                break
            # Process the keys left as additional information or superseeding values for the term.
            if term_specs_from_collection:
                term_from_universe = term_from_universe.model_copy(update=term_specs_from_collection, deep=True)
            result[collection_name][term_id] = term_from_universe
    return result


def _parse_projects(parent_projects_dir_path: Path) -> dict[str : dict[str : dict[str:BaseModel]]]:
    result = dict()
    for project_dir_path in parent_projects_dir_path.iterdir():
        _LOGGER.debug(f"parse project: {project_dir_path}")
        result[project_dir_path.name] = _parse_collections_of_project(project_dir_path)
    return result


# dict[datadescriptor_name: dict[term id, term object]
TERMS_OF_UNIVERSE: dict[str, dict[str, BaseModel]] = _parse_terms_of_universe(settings.UNIVERSE_DIR_PATH)

# dict[project_name: dict[collection_name: dict[term_id: term object]]]
TERMS_OF_COLLECTIONS_OF_PROJECTS: dict[str : dict[str : dict[str:BaseModel]]] = _parse_projects(
    settings.PROJECTS_PARENT_DIR_PATH
)
