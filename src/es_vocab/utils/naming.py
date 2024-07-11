from pathlib import Path

from es_vocab.utils.constants import (
    DIRNAME_AND_FILENAME_SEPARATOR,
    PYDANTIC_MODEL_DIRNAME,
)


def from_pydantic_module_filepath_to_pydantic_class_name(file_path: Path) -> str:
    splits = file_path.stem.split(DIRNAME_AND_FILENAME_SEPARATOR)
    return "".join([split.capitalize() for split in splits])


def compute_pydantic_file_path_from_data_descriptor_dir_path(dir_path: Path) -> Path:
    return dir_path.joinpath(PYDANTIC_MODEL_DIRNAME).joinpath(f"{dir_path.name}.py")
