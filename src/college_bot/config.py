from pydantic_settings import BaseSettings
from pydantic import SecretStr, Field
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr = Field(..., validation_alias="BOT_TOKEN")

    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DB_CONFIG(self) -> dict:
        return {
            'host': self.DB_HOST, 
            'user': self.DB_USER, 
            'password': self.DB_PASSWORD, 
            'db': self.DB_NAME,
        }

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = 'utf-8'

settings = Settings()