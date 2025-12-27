import uuid
from collections.abc import Sequence
from io import BytesIO
from typing import Annotated, Literal

import filetype
from fastapi import APIRouter, File, UploadFile
from PIL import Image

from Services.TemplateApiServise.Application.exceptions.BaseApiError import BaseApiError
from Services.TemplateApiServise.Persistence.Repository.S3.MinioRepository import s3_manager

simple_storage_service_router = APIRouter()
MAX_FILE_SIZE = 15 * 1024 * 1024
ALLOWED_EXTENSIONS: Sequence[str] = ("image/png", "image/jpg", "image/jpeg", "image/gif", "image/webp")


@simple_storage_service_router.post("/file", name="upload file", status_code=200)
async def upload_file(bucket_name: Literal["general"], file: Annotated[UploadFile, File(...)]):
    if not (file.filename and file.content_type and file.size):
        raise BaseApiError(
            status_code=409,
            error="FILE_NOT_SUPPORTED",
            message="filename and content_type and size are required",
            detail={"filename": file.filename, "content_type": file.content_type, "size": file.size},
        )
    elif file.content_type in ALLOWED_EXTENSIONS:
        raise BaseApiError(
            status_code=400,
            error="FILE_NOT_SUPPORTED",
            message="File not in supported format",
            detail={"content_type": file.content_type, "allowed_extensions": ALLOWED_EXTENSIONS},
        )
    elif file.size > MAX_FILE_SIZE:
        raise BaseApiError(
            status_code=400,
            error="FILE_NOT_SUPPORTED",
            message="File size too large 15 mb",
            detail={"filename": file.filename, "content_type": file.content_type, "size": file.size},
        )

    object_bytes = await file.read()
    object_data = BytesIO(object_bytes)
    content_type = filetype.guess(object_bytes)
    if content_type in ["image/jpeg", "image/png", "image/jpg"]:
        img = Image.open(object_data)
        object_data = BytesIO()
        img.save(object_data, format="WEBP")
        content_type = "image/webp"

    object_data.seek(0)
    return await s3_manager.upload(
        body=object_data,
        object_name=f"{uuid.uuid4().hex}",
        bucket_name=bucket_name,
        content_type=content_type,
    )
