from typing import List, Annotated
from content.models import ContentOut, ContentOutList, ContentIn
from users.services import get_current_active_user
from users.models import User
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, Query
import content.services as ContentServices

from fastapi import APIRouter


content_router = APIRouter(prefix='/content', tags=['content'])


@content_router.post("", response_model=ContentOut)
async def post_content(current_user: Annotated[User, Depends(get_current_active_user)],
                       content: ContentIn):
    return await ContentServices.post_content(current_user, content)

# @user_router.post("/login", response_model=UserOut)
# async def update_user(current_user: Annotated[User, Depends(get_current_active_user)]):
#     return await UserServices().update_user(id, current_user)


# @user_router.get("", response_model=UserOutList)
# async def read_user_by(current_user: Annotated[User, Depends(get_current_active_user)],
#                         skip: int = 0, limit: int | None = 100,
#                         user_id: int | None = None):
#     obj = await UserServices().read_users(current_user,
#                                          skip, limit, user_id)
#     return {"rows" : obj, "meta" : {"skip" : skip, "limit" : limit, "count" : len(obj)}}


# @user_router.patch("", response_model=UserOut)
# async def update_user(id: int,
#                       user: UserUpdate,
#                       current_user: Annotated[User, Depends(get_current_active_user)]):
#     return await UserServices().update_user(id, user, current_user)


# @user_router.delete("")
# async def delete_user_by_id(id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
#     return await UserServices().delete_user(id, current_user)


# @token_router.post("", response_model=Token)
# async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     return await UserServices().login_for_access_token(form_data)
