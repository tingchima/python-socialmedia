from typing import TypeVar

from django.db import models
from django.db.models import Model

ModelType = TypeVar("ModelType", bound=Model)


class Base(models.Model):
    """Represents a base model."""

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
