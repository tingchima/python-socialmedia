from account.router.v1.token_router import router as v1_token_router
from account.router.v1.user_router import router as v1_user_router
from ninja import Router

v1_group = Router()

"""
Account API v1
"""

v1_group.add_router("/token", v1_token_router, tags=["token"])
v1_group.add_router("/users", v1_user_router, tags=["user"])
