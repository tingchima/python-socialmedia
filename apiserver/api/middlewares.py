import logging
import time
from uuid import uuid4

from account.containers import token_service
from ninja.security import APIKeyHeader, HttpBearer


class AccessLogger:
    """Represents a middleware of access logger."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.info(f"api incoming request: {request.method} {request.path}")
        response = self.get_response(request)
        logging.info(f"api outgoing response: {response.status_code} {response.content}")
        return response


class RequestID:
    """Represents a middleware of request id."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = uuid4()
        response = self.get_response(request)
        response["x-request-id"] = request_id
        return response


class ProcessTime:
    """Represents a middleware of request process time middleware."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        process_time = time.time() - start_time
        response["x-process-time"] = str(process_time)
        return response


class ExceptionNotification:
    """Represets a middleware of exception notification middleware."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response


class XClinetID(APIKeyHeader):
    """Represents a middleware of x-client-id."""

    param_name = "X-Client-ID"

    def authenticate(self, request, key):
        if token_service.client_id_verify(key):
            request.client_id = key
            return key


x_client_id_required = XClinetID()


# ref. https://django-ninja.dev/guides/authentication/?h=security
class BearerToken(HttpBearer):
    """Represnets a middleware of bearer token."""

    def authenticate(self, request, token):
        client_id = x_client_id_required(request)
        request.current_user = token_service.token_verify(token, client_id)
        return request.current_user


bearer_token_required = BearerToken()
