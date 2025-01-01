from fastapi import APIRouter

from Services.UserService.Users.router import users_router

router = APIRouter()

router.include_router(users_router, tags=['User | Users'], prefix='/users')
