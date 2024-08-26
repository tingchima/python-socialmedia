from dataclasses import dataclass
from typing import TypeVar


@dataclass
class Entity:
    """Represents a entity."""


EntityType = TypeVar("EntityType", bound=Entity)
