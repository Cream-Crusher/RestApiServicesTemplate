import io
import uuid
from enum import StrEnum
from io import BytesIO
from typing import Annotated, Literal
from PIL import Image

from fastapi import APIRouter, File, HTTPException, UploadFile

from Services.TemplateApiServise.Persistence.Repository.S3.MinioRepository import s3_manager

simple_storage_service_router = APIRouter()
MAX_FILE_SIZE = 15 * 1024 * 1024


class ConvertFormatEnum(StrEnum):
    webp = "WEBP"
    jpg = "JPG"
    gif = "GIF"
    png = "PNG"


@simple_storage_service_router.post("/file", name="upload file", status_code=200)
async def upload_file(bucket_name: Literal["general"], file: Annotated[UploadFile, File(...)]):
    if not (file.filename and file.content_type and file.size):
        raise HTTPException(409)

    if file.size > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large 15 mb")

    object_data = BytesIO(await file.read())
    object_data.seek(0)

    return await s3_manager.upload(
        body=object_data,
        object_name=f"{uuid.uuid4()}:{file.filename}",
        bucket_name=bucket_name,
        content_type=file.content_type,
    )


@simple_storage_service_router.post("/file/convert/{format}", name="convert file", status_code=200)
async def convert_file(bucket_name: Literal["general"], file: Annotated[UploadFile, File(...)], format: ConvertFormatEnum):
    from PIL import Image

    if not (file.filename and file.content_type and file.size):
        raise HTTPException(409)

    if file.size > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large 15 mb")

    file_size = await file.read()
    bytes_io = BytesIO(file_size)
    img = Image.open(bytes_io)
    bytes_io_output = BytesIO()
    img.save(bytes_io_output, format=format)
    object_data = BytesIO(bytes_io_output.getvalue())
    object_data.seek(0)

    return await s3_manager.upload(
        body=object_data,
        object_name=f"{uuid.uuid4()}:{file.filename}",
        bucket_name=bucket_name,
        content_type=file.content_type,
    )
