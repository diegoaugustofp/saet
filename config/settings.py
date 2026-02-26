"""Configuracoes centralizadas do SAET usando Pydantic Settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuracoes globais do SAET."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="SAET_",
        case_sensitive=False,
    )
    
    # Aplicacao
    app_name: str = "SAET"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Banco de dados
    database_url: str = "sqlite+aiosqlite:///saet.db"
    
    # API   
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Seguranca
    encryption_key: str = ""
    
    # Scheduler
    default_interval_minutes: int = 5
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"


@lru_cache
def get_settings() -> Settings:
    """Retorna instancia singleton das configuracoes."""
    return Settings()