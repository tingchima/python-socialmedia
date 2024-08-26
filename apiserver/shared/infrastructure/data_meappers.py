from typing import List

from ..domain.entities import EntityType
from ..models import ModelType


class DataMapper:
    """Represents a data mapper."""

    def entity_to_model(self, entity: EntityType) -> ModelType:
        raise NotImplementedError

    def model_to_entity(self, model: ModelType) -> EntityType:
        raise NotImplementedError

    def model_to_entity_list(self, models: List[ModelType]) -> List[EntityType]:
        return [self.model_to_entity(model=i) for i in models]


class JsonDataMapper:
    """Represents a data mapper of json."""

    def entity_to_json_data(self, entity: EntityType) -> dict:
        raise NotImplementedError

    def json_data_to_entity(self, data: dict, entity_cls: EntityType) -> EntityType:
        raise NotImplementedError

    def json_data_to_entity_list(self, data: List[dict]) -> List[EntityType]:
        return [self.json_data_to_entity(data=i) for i in data]
