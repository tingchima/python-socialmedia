from api.middlewares import bearer_token_required
from chat.containers import chatroom_service
from chat.domain.entities import Chatroom
from chat.domain.enums import RoomType
from chat.router.schemas import (
    ChatroomCreateBody,
    ChatroomCreateResponse,
    ChatroomGetResposne,
    ChatroomJoinPath,
    ChatroomListQuery,
    ChatroomListResponse,
)
from ninja import Path, Query, Router
from shared.router.pagination import to_next_offset
from shared.router.response import ErrorResponse, Response, to_response

router = Router(auth=bearer_token_required)


@router.get(
    "",
    response={
        200: Response[ChatroomListResponse],
        401: Response[ErrorResponse],
        500: Response[ErrorResponse],
    },
)
def chatroom_list(request, query: Query[ChatroomListQuery]):
    rooms, total_size = chatroom_service.chatrooms_of_user(
        user_id=request.current_user.id, offset=query.offset, limit=query.limit
    )
    return to_response(
        200,
        ChatroomListResponse.build(
            rooms=rooms,
            next_offset=to_next_offset(
                total_size=total_size, offset=query.offset, limit=query.limit
            ),
        ),
    )


@router.get(
    "/{room_id}",
    response={
        200: Response[ChatroomGetResposne],
        401: Response[ErrorResponse],
        403: Response[ErrorResponse],
        404: Response[ErrorResponse],
        500: Response[ErrorResponse],
    },
)
def chatroom_get(request, room_id: int):
    room = chatroom_service.chatroom_get(room_id=room_id, user_id=request.current_user.id)
    return to_response(200, ChatroomGetResposne.build(room))


@router.post(
    "",
    response={
        201: Response[ChatroomCreateResponse],
        401: Response[ErrorResponse],
        500: Response[ErrorResponse],
    },
)
def chatroom_create(request, body: ChatroomCreateBody):
    param = Chatroom(
        room_name=body.room_name,
        avatar_url=body.avatar_url,
        room_type=RoomType[body.room_type].name,
    )
    room = chatroom_service.chatroom_create(param)
    return to_response(201, ChatroomCreateResponse.build(room))


@router.post(
    "/{room_id}",
    response={
        204: None,
        401: Response[ErrorResponse],
        404: Response[ErrorResponse],
        409: Response[ErrorResponse],
        500: Response[ErrorResponse],
    },
)
def chatroom_join(request, path: Path[ChatroomJoinPath]):
    chatroom_service.chatroom_join(room_id=path.room_id, user_id=request.current_user.id)
    return 204, None
