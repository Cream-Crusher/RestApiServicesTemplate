import io

from Services.TelegramBotService.get_bot import get_bot
from Services.TemplateApiServise.Persistence.Repository.S3.MinioRepository import s3_manager


@alru_cache
async def get_bot_file_url(
        file_id: str,
        content_type: str = "image/png"
) -> str:
    bot = get_bot()
    object_data = io.BytesIO()
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, object_data)
    object_data.seek(0)

    file_url = await s3_manager.update(object_data, f"{file_id}.png", "user-avatar", content_type)

    return file_url
