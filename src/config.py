from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath
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
    project_config = SettingsConfigDict(env_file='/.env',
                                      env_file_encoding='utf-8')
    log_filename: str
    log_level: str

settings = Settings()
logger.add(settings.log_filename,
           level=settings.log_level,)
