import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Any, Union


class MaterialType(str, Enum):
    article = "article"
    video = "video"


@dataclass
class Material:
    id: int
    description: str = None
    additional_properties: Union[dict, list, tuple, Any] = None
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = None


@dataclass
class Material2:
    id: int
    description: str = None
    additional_properties: Union[dict, list] = None
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = None
