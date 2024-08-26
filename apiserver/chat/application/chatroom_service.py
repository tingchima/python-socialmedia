from chat.domain.entities import Chatroom, ChatroomMember
from chat.infrastructure.mysql.chatroom_member_repository import ChatroomMemberRepository
from chat.infrastructure.mysql.chatroom_repository import ChatroomRepository
from shared.domain.errors import ForbiddenError, NotFoundError


class ChatroomService:
    """Represents a service of chatroom."""

    chatroom_repo: ChatroomRepository = ChatroomRepository()
    chatroom_member_repo: ChatroomMemberRepository = ChatroomMemberRepository()

    def _member_exists_of_user(self, room_id: int, user_id: int):
        exist = self.chatroom_member_repo.member_exists_of_user(room_id=room_id, user_id=user_id)
        if not exist:
            raise ForbiddenError(
                f"there is not a member {user_id} from specified {room_id} chatroom"
            )
        return True

    def _room_exists(self, room_id: int):
        exists = self.chatroom_repo.chatroom_exists_by_id(id=room_id)
        if not exists:
            raise NotFoundError(f"specified {room_id} chatroom is not found")

    def chatroom_create(self, param: Chatroom) -> Chatroom:
        room = self.chatroom_repo.save(param)
        return room

    def chatroom_get(self, room_id: int, user_id: int) -> Chatroom:
        self._member_exists_of_user(room_id=room_id, user_id=user_id)
        room = self.chatroom_repo.get_by_key(id=room_id)
        return room

    def chatroom_join(self, room_id: int, user_id: int):
        self._room_exists(room_id=room_id)
        room_member = ChatroomMember(room_id=room_id, user_id=user_id)
        _ = self.chatroom_member_repo.save(room_member)  # push notification by different room type
        # create join system message
        return

    def chatrooms_of_user(self, user_id: int, offset: int, limit: int):
        rooms, total_size = self.chatroom_repo.chatrooms_of_user(
            user_id=user_id, offset=offset, limit=limit
        )
        return rooms, total_size
