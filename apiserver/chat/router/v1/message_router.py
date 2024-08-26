from api.middlewares import bearer_token_required
from chat.containers import message_service
from ninja import Query, Router
from shared.router.response import ErrorResponse, Response, to_response

from ..schemas import (
    MessageCreateBody,
    MessageCreateResponse,
    MessageDeleteBody,
    MessageListQuery,
    MessageListResponse,
)

router = Router(auth=bearer_token_required)


@router.get(
    "",
    response={
        200: Response[MessageListResponse],
        401: Response[ErrorResponse],
        403: Response[ErrorResponse],
        500: Response[ErrorResponse],
    },
)
def messages_list_of_room(request, query: Query[MessageListQuery]):
    messages, last_timesatmp = message_service.messages_of_room(
        room_id=query.room_id, user_id=request.current_user.id, last_timestamp=query.last_timestamp
    )
    return to_response(200, MessageListResponse.build(messages, last_timesatmp))


@router.post(
    "",
    response={
        201: Response[MessageCreateResponse],
        401: Response[ErrorResponse],
        403: Response[ErrorResponse],
        500: Response[ErrorResponse],
    },
)
def message_create(request, body: MessageCreateBody):
    user_id = request.current_user.id
    message = message_service.message_create(room_id=body.room_id, user_id=user_id, text=body.text)
    return to_response(201, MessageCreateResponse.build(message))


@router.delete(
    "",
    response={
        204: None,
        401: Response[ErrorResponse],
        403: Response[ErrorResponse],
        500: Response[ErrorResponse],
    },
)
def message_delete(request, body: MessageDeleteBody):
    user_id = request.current_user.id
    message_service.message_delete(
        room_id=body.room_id, user_id=user_id, created_timestamp=body.created_timestamp
    )
    return 204, None
