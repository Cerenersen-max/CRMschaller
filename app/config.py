"""Uygulama genelinde kullanilan ayarlar. .env dosyasindan okunur."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    secret_key: str = "change-me"
    database_url: str = "sqlite:///./crmschaller.db"

    # Banka / Open Banking
    nordea_client_id: str = ""
    nordea_client_secret: str = ""
    nordea_api_base_url: str = "https://api.nordeaopenbanking.com"
    isbank_api_key: str = ""
    isbank_api_base_url: str = ""
    kuveytturk_api_key: str = ""
    kuveytturk_api_base_url: str = ""
    fx_rate_api_url: str = "https://api.exchangerate.host/latest"

    # Muhasebe entegrasyonu
    accounting_api_url: str = ""
    accounting_api_key: str = ""

    # Telegram bot
    telegram_bot_token: str = ""
    telegram_allowed_chat_ids: str = ""

    # Kubernetes
    kube_config_path: str = ""
    kube_namespace: str = "default"

    # Syslog
    syslog_host: str = "localhost"
    syslog_port: int = 514

    @property
    def telegram_allowed_chat_id_list(self) -> list[int]:
        return [
            int(chat_id)
            for chat_id in self.telegram_allowed_chat_ids.split(",")
            if chat_id.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
