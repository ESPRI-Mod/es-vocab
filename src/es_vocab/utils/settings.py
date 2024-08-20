import logging
import sys
from pathlib import Path

#################################### CONSTANTS ######################################

DIRNAME_AND_FILENAME_SEPARATOR = "_"

# Paths in universe repository:
UNIVERSE_DIR_PATH = Path("../WGCM_CVs")
DATA_DESCRIPTORS_PARENT_DIR_PATH = UNIVERSE_DIR_PATH.joinpath("data_descriptors")
PYDANTIC_MODEL_DIRNAME = "models"
TERMS_DIRNAME = "terms"

# Paths in project repositories:
PROJECTS_PARENT_DIR_PATH = Path("../projects")
COLLECTIONS_DIRNAME = "collections"

# RDF:
GRAPH_DIRNAME = "graph"
GRAPH_DIR_PATH = UNIVERSE_DIR_PATH.joinpath(GRAPH_DIRNAME)

# JSON-LD node names:
COLLECTION_TERM_SPECS_LIST_NODE_NAME = "@graph"
ID_NODE_NAME = "@id"
TYPE_NODE_NAME = "@type"

SECRET_TOKEN = "tobereplaced"  # TODO: to be replaced!

# API Server settings
API_SERVER_DOMAINE_NAME = "es-vocab.ipsl.fr"

#################################### LOGGING ########################################

LOG_HANDLERS = [logging.StreamHandler(sys.stdout)]
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_LEVEL = logging.DEBUG

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, handlers=LOG_HANDLERS)

############################# NAMING RULE FUNCTIONS #################################


def from_pydantic_module_filepath_to_pydantic_class_name(file_path: Path) -> str:
    splits = file_path.stem.split(DIRNAME_AND_FILENAME_SEPARATOR)
    return "".join([split.capitalize() for split in splits])


def compute_pydantic_file_path_from_data_descriptor_dir_path(dir_path: Path) -> Path:
    return dir_path.joinpath(PYDANTIC_MODEL_DIRNAME).joinpath(f"{dir_path.name}.py")


def compute_terms_dir_path_from_data_descriptor_dir_path(dir_path: Path) -> Path:
    return dir_path.joinpath(TERMS_DIRNAME)


def from_collection_file_path_to_collection_id(file_path: Path) -> str:
    return file_path.stem
