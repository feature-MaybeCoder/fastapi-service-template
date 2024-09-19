"""
A module with app config
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DB_URI: str


settings = Settings()
