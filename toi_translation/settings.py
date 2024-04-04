from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingCfg(BaseSettings):
    model_config = SettingsConfigDict(env_file=".config.env", env_file_encoding="utf-8")

    JSON_LOGS: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="DEBUG")
    UVICORN_RELOAD: bool = Field(default=True)

    GEMINI_MODEL: str = Field(default="gemini-pro")


class SettingEnv(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    GOOGLE_API_KEY: str = Field(default="")


setting_cfg = SettingCfg()
setting_env = SettingEnv()
