import importlib.util
import inspect
import logging
from pathlib import Path

from pydantic import BaseModel

from es_vocab.utils.naming import (
    compute_pydantic_file_path_from_data_descriptor_dir_path,
    from_pydantic_module_filepath_to_pydantic_class_name,
)

_LOGGER = logging.getLogger("cvs_parser")


def _get_classes_from_module(module) -> dict[str, type]:
    # inspect.getmembers to get all classes defined in the module.
    classes = inspect.getmembers(module, inspect.isclass)
    # Filter out classes that are not defined in this module
    module_classes = {name: cls for name, cls in classes if cls.__module__ == module.__name__}
    return module_classes


def _load_pydantic_class(pydantic_module_file_path: Path) -> type:
    class_name = from_pydantic_module_filepath_to_pydantic_class_name(pydantic_module_file_path)
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


def parse_terms_of_universe(parent_dir_path: Path) -> dict[str, dict[str, BaseModel]]:
    result = dict()

    for dir_path in parent_dir_path.iterdir():
        _LOGGER.debug(f"parse dir {dir_path}")
        result[dir_path.name] = dict()
        pydantic_class_module_file_path = compute_pydantic_file_path_from_data_descriptor_dir_path(dir_path)
        pydantic_class = _load_pydantic_class(pydantic_class_module_file_path)
        _LOGGER.debug(f"found pydantic class: {pydantic_class}")
        for file_path in dir_path.glob("**/*.json"):
            _LOGGER.debug(f"parse file {file_path}")
            try:
                json_content_file = Path(file_path).read_text()
                pydantic_instance = pydantic_class.model_validate_json(json_content_file)
                result[dir_path.name][pydantic_instance.id] = pydantic_instance
            except Exception as e:
                _LOGGER.error(f"unable to parse {file_path}:\n{str(e)}")
    return result
