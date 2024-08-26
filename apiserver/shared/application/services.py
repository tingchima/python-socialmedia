from shared.domain.entities import Entity
from shared.infrastructure.repositories import DjangoRepository


def entity_update(instance_repository: DjangoRepository, instance_entity: Entity) -> Entity:
    entity = instance_repository.save(entity=instance_entity)
    return entity
