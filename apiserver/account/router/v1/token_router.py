from account.containers import token_service
from api.middlewares import bearer_token_required
from ninja import Router
from shared.router.response import Response, to_response

from ..schemas import TokenCreateBody, TokenCreateResponse, TokenRefreshBody

router = Router()


@router.post(
    "",
    response={
        200: Response[TokenCreateResponse],
    },
)
def token_create(request, body: TokenCreateBody):

    token = token_service.token_create(
        email=body.email,
        client_id=body.client_id,
    )

    return to_response(200, TokenCreateResponse.build(token))


@router.post(
    "/refresh",
    response={
        200: Response[TokenCreateResponse],
    },
    auth=bearer_token_required,
)
def token_refresh(request, body: TokenRefreshBody):

    token = token_service.token_refresh(
        token=body.refresh_token,
        client_id=request.client_id,
    )

    return to_response(200, TokenCreateResponse.build(token))
