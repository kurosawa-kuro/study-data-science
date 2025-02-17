import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environmental variables from .env file
load_dotenv()  # .envファイルから環境変数を読み込む

DATABASE_URL = os.getenv("DB_URL")
if not DATABASE_URL:
    raise Exception("DB_URL is not set in the environment (.env file)")

engine = create_engine(DATABASE_URL)
