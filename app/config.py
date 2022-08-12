from pydantic import BaseSettings, PostgresDsn, RedisDsn, Field, PositiveInt
from os import path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    pg_dsn: PostgresDsn = Field(..., env='DB_URL')
    redis_dsn: RedisDsn = Field(..., env='REDIS_CACHE_URL')

    debug: bool = Field(True, env='DEBUG')

    host: str = Field('localhost', env='HOST')
    port: PositiveInt = Field(8001, env='PORT')

    class Config:
        env_file = path.join(BASE_DIR, '.env')  # в контейнер через compose
        env_file_encoding = 'utf-8'


settings = Settings()
