from abc import ABC, abstractmethod
from typing import Any, Generic

from boto3.dynamodb.table import TableResource
from boto3.exceptions import Boto3Error
from django.db import DatabaseError
from shared.domain.errors import InternalServerError, NotFoundError

from ..domain.entities import EntityType
from ..models import ModelType
from .data_meappers import DataMapper, JsonDataMapper


def offset_and_limit_to_start_and_end_index(offset: int, limit: int):
    start = (offset - 1) * limit
    end = start + limit
    return start, end


class AbstractRepository(Generic[EntityType], ABC):
    """Represents a repository of abstract."""

    @abstractmethod
    def save(self, entity: EntityType) -> EntityType:
        raise NotImplementedError()

    @abstractmethod
    def get_by_key(self, key: Any) -> EntityType:
        raise NotImplementedError()

    @abstractmethod
    def delete_by_key(self, key: Any):
        raise NotImplementedError()


class DjangoRepository(AbstractRepository):
    """Represents a repository of django."""

    data_mapper_cls: type[DataMapper]
    model_cls: type[ModelType]

    # usage: create, update model
    def save(self, entity: EntityType) -> EntityType:
        try:
            model: ModelType = self.data_mapper.entity_to_model(entity=entity)
            model.save()
            return self.data_mapper.model_to_entity(model=model)
        except DatabaseError as e:
            raise InternalServerError(e)

    def get_by_key(self, id: int) -> EntityType:
        try:
            model: ModelType = self.model().objects.get(id=id)
            return self.data_mapper.model_to_entity(model=model)
        except self.model().DoesNotExist as e:
            raise NotFoundError(e)

    def delete_by_key(self, id: int):
        try:
            model: ModelType = self.model().objects.get(id=id)
            model.delete()
        except self.model().DoesNotExist as e:
            raise NotFoundError(e)
        except DatabaseError as e:
            raise InternalServerError(e)

    @property
    def data_mapper(self):
        return self.data_mapper_cls()

    def model(self):
        return self.model_cls


class Boto3Repository(AbstractRepository, ABC):
    """Represnets a repository of dynamodb."""

    table_cls: type[TableResource]
    data_mapper_cls: type[JsonDataMapper]

    def save(self, entity: EntityType) -> EntityType:
        try:
            json_data: dict = self.data_mapper.entity_to_json_data(entity=entity)
            self.table().put_item(Item=json_data)
            return self.data_mapper.json_data_to_entity(data=json_data)
        except Boto3Error as e:
            raise InternalServerError(e)

    def get_by_key(self, key: dict) -> EntityType:
        try:
            json_data = self.table().get_item(Key=key)
            return self.data_mapper.json_data_to_entity(data=json_data.pop("Item"))
        except Boto3Error as e:
            raise InternalServerError(e)

    def delete_by_key(self, key: dict):
        try:
            self.table().delete_item(Key=key)
        except Boto3Error as e:
            raise InternalServerError(e)

    @abstractmethod
    def key(self, data: Any) -> dict:
        raise NotImplementedError

    @property
    def data_mapper(self):
        return self.data_mapper_cls()

    def table(self) -> TableResource:
        return self.table_cls
