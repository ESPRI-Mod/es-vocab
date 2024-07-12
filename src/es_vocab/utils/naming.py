from pathlib import Path

DIRNAME_AND_FILENAME_SEPARATOR = "_"

# Paths:
UNIVERSE_DIR_PATH = Path("../universe")
PROJECTS_PARENT_DIR_PATH = Path("../projects")
PYDANTIC_MODEL_DIRNAME = "models"

# JSON-LD node names:
COLLECTION_TERM_SPECS_LIST_NODE_NAME = "@graph"
ID_NODE_NAME = "@id"
TYPE_NODE_NAME = "@type"


def from_pydantic_module_filepath_to_pydantic_class_name(file_path: Path) -> str:
    splits = file_path.stem.split(DIRNAME_AND_FILENAME_SEPARATOR)
    return "".join([split.capitalize() for split in splits])


def compute_pydantic_file_path_from_data_descriptor_dir_path(dir_path: Path) -> Path:
    return dir_path.joinpath(PYDANTIC_MODEL_DIRNAME).joinpath(f"{dir_path.name}.py")


def from_collection_file_path_to_collection_name(file_path: Path) -> str:
    return file_path.stem
