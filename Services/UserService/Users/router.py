from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from Services.UserService.Users.schema import UserRead, UserCreate
from Services.UserService.Users.service import user_repository
from Shared.Auth.telegram_authentication import get_me as get_current_user

users_router = APIRouter()


@users_router.post('', name='create', status_code=201)
async def create(user_create_dto: UserCreate, user_service=user_repository):
    await user_service.create(user_create_dto)

    return JSONResponse(
        content={"message": "Success"},
        status_code=status.HTTP_201_CREATED,
        media_type="application/json"
    )


@users_router.get('/all', name='get all users', response_model=list[UserRead], status_code=200)
async def get_all(user_service=user_repository):
    users = await user_service.all()
    return users


@users_router.get('/me', name='get me', response_model=UserRead)
async def get_me(user=Depends(get_current_user)):
    return user
