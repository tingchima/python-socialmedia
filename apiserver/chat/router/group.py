from chat.router.v1.chatroom_router import router as v1_chatroom_router
from chat.router.v1.message_router import router as v1_message_router
from ninja import Router

v1_group = Router()

"""
Chat API v1
"""

v1_group.add_router("/chatrooms", v1_chatroom_router, tags=["chatrooms"])
v1_group.add_router("/messages", v1_message_router, tags=["messages"])

"""
Chat API v2
"""
# v2_group = Router()
