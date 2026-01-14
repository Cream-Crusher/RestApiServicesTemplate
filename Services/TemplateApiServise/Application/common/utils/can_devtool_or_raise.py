from config import EnvironmentEnum, config
from Services.TemplateApiServise.Application.common.exceptions.BaseApiError import BaseApiError


def can_devtool_or_raise():
    if config.app_config.environment == EnvironmentEnum.PROD:
        raise BaseApiError(403, "DevToolNotAllowed", "devtool not allowed in production environment")
