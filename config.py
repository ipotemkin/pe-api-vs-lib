"""Модуль конфигурации приложения на базе pydantic-settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Настройки приложения."""
    
    # GigaChat API credentials
    gigachat_client_id: str
    gigachat_client_secret: str
    gigachat_scope: str = "GIGACHAT_API_PERS"
    
    # GigaChat API URLs
    gigachat_oauth_url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    gigachat_chat_completions_url: str = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = AppSettings()
