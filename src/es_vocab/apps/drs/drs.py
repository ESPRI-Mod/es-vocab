from pydantic import BaseModel, Field
from enum import Enum
from typing import Literal, Annotated


class DrsType(str, Enum):
    directory = "directory"
    filename = "filename"
    dataset_id = "dataset_id"


class DrsPartType(str, Enum):
    constant = "constant"
    collection = "collection"


class DrsConstantPart(BaseModel):
    value: str
    kind: Literal[DrsPartType.constant] = DrsPartType.constant


class DrsCollectionPart(BaseModel):
    collection_name: str
    is_required: bool
    kind: Literal[DrsPartType.collection] = DrsPartType.collection


DrsPart = Annotated[DrsConstantPart | DrsCollectionPart, Field(discriminator="kind")]


class DrsSpecification(BaseModel):
    type: DrsType
    separator: str
    parts: list[DrsPart]
