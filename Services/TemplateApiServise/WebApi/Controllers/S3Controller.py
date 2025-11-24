import uuid
from io import BytesIO
from typing import Annotated, Literal

import filetype
from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image

from Services.TemplateApiServise.Persistence.Repository.S3.MinioRepository import s3_manager

simple_storage_service_router = APIRouter()
MAX_FILE_SIZE = 15 * 1024 * 1024


@simple_storage_service_router.post("/file", name="upload file", status_code=200)
async def upload_file(bucket_name: Literal["general"], file: Annotated[UploadFile, File(...)]):
    if not (file.filename and file.content_type and file.size):
        raise HTTPException(409)

    if file.size > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large 15 mb")

    object_bytes = await file.read()
    object_data = BytesIO(object_bytes)
    content_type = filetype.guess(object_bytes)
    if content_type in ["image/jpeg", "image/png"]:
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
