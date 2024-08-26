from typing import Generic, TypeVar

from ninja import Schema

ResultType = TypeVar("ResultType")


class Response(Schema, Generic[ResultType]):
    """Representsa a response."""

    data: ResultType


def to_response(status_code: int, data: dict | list):
    return status_code, {"data": data}


class ErrorResponse(Schema):
    """Represents a error reponse."""

    client_message: str
