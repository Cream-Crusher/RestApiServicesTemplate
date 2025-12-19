import uuid
from datetime import datetime, timedelta

import bcrypt
import jose
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel

from config import config
from Services.TemplateApiServise.Application.common.utcnow import utcnow
from Services.TemplateApiServise.Application.exceptions.BaseApiError import BaseApiError

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=config.oauth2.token_url, scheme_name=config.oauth2.scheme_name, auto_error=False
)

ALGORITHM = config.oauth2.algorithm
KEY = config.oauth2.key


class AdminDTO(BaseModel):
    id: uuid.UUID
    display_name: str


def create_access_token(admin: AdminDTO):
    expire = utcnow() + timedelta(days=3)
    encoding = admin.model_dump(mode="json") | {"exp": expire}
    encoded_jwt = jwt.encode(encoding, KEY, algorithm=ALGORITHM)
    return encoded_jwt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_me_admin(token: str = Depends(oauth2_scheme)) -> AdminDTO:
    if not token:
        raise BaseApiError(
            status_code=401, error="TOKEN_NOT_PROVIDED", message="Token not provided", detail={"token": token}
        )
    try:
        payload = jwt.decode(token=token, key=KEY, algorithms=[ALGORITHM])

    except jose.ExpiredSignatureError:
        raise BaseApiError(
            status_code=401, error="TOKEN_EXPIRED", message="Token has expired", detail={"token": token}
        )

    except Exception as e:
        raise BaseApiError(
            status_code=401, error="INVALID_TOKEN", message="Invalid token", detail={"error": str(e), "token": token}
        )

    if payload.get("exp") and payload["exp"] < datetime.timestamp(utcnow()):
        raise BaseApiError(
            status_code=401, error="TOKEN_EXPIRED", message="Token has expired", detail={"token": token}
        )

    return AdminDTO(**payload)
