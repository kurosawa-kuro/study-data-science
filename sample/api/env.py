from pydantic_settings import BaseSettings
from pydantic import Field  # Use pydantic's Field for aliasing

class Environment(BaseSettings):
    """環境変数を定義する構造体。
    pydanticを利用した環境変数の読み込み: https://fastapi.tiangolo.com/advanced/settings/#environment-variables
    """
    db_user: str = ""
    db_password: str = ""
    db_port: str = ""
    db_host: str = ""
    db_name: str = "chapter11"

    token_expire_minutes: int = 480
    token_secret_key: str = "1234567890"
    token_algorithm: str = "HS256"

    db_url: str = Field(..., env="DB_URL")

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # .env に定義されている不要な変数は無視する

# Instantiate the settings from the .env file.
env = Environment()

# This variable is used across the app for creating the database engine.
SQLALCHEMY_DATABASE_URL = env.db_url