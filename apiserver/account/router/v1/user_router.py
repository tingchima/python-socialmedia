from account.containers import user_service
from account.domain.entities import User as User
from account.domain.enums import UserType
from ninja import Router
from shared.router.response import Response, to_response

from ..schemas import UserCreateBody, UserCreateReponse

router = Router()


@router.post(
    "",
    response={
        201: Response[UserCreateReponse],
        # 500:
    },
)
def user_create(request, body: UserCreateBody):
    try:
        user_param = User.new(
            email=body.email,
            username=body.username,
            password=body.password,
            avatar_url=body.avatar_url,
            user_type=UserType[body.user_type].name,
        )
        user = user_service.user_create(param=user_param)
    except Exception as e:
        print(f"error={e}")
        raise e
    return to_response(201, UserCreateReponse.build(user))
