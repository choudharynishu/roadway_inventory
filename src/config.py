from pydantic_settings import BaseSettings, SettingsConfigDict
from dataclasses import dataclass
from pathlib import Path
from loguru import logger


@dataclass
class Config():
    size: str
    fov: int
    headings: list
    pitch: int
    api_key: str
    output_dir: Path


class LogSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='log/.env',
                                      env_file_encoding='utf-8')
    log_filename: str
    log_level: str


class ModelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='model/.env.model',
                                      env_file_encoding='utf-8')
    model_dir: str
    model_version: str
    num_epochs: int
    image_size:int
    device: str
    best_model_dir: str


class DataSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='data/.env.data',
                                      env_file_encoding='utf-8')
    train_dir: str
    data_yaml: str
    inference_filename: str

logsettings = LogSettings()
logger.add(logsettings.log_filename,
           level=logsettings.log_level,)

modelsettings = ModelSettings()

datasettings = DataSettings()
