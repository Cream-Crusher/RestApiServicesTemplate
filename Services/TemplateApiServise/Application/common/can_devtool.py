from config import settings, EnvironmentEnum


def can_devtool():
    assert settings.app_config.environment in [EnvironmentEnum.LOCAL, EnvironmentEnum.DEV]
