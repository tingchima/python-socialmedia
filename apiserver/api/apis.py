from account.router.group import v1_group as account_v1_router_group
from chat.router.group import v1_group as chat_v1_router_group
from ninja import NinjaAPI

from .error_handlers import ErrorHandlerAdater

router = NinjaAPI()

ErrorHandlerAdater(router)


router.add_router("v1/", account_v1_router_group)
router.add_router("v1/", chat_v1_router_group)
