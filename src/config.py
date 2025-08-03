from pydantic_settings import BaseSettings, SettingsConfigDict
from dataclasses import dataclass
from pathlib import Path
from loguru import logger


@dataclass
class config():
    size: int
    fov: int
    headings: list
    pitch: int
    api_key: str
    output_dir: Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8')
    api_key: str
    log_filename: str
    log_level: str

settings = Settings()
logger.add(settings.log_filename,
           level=settings.log_level,)
