from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from env import Environment  # 環境変数設定のためのクラスを読み込み

env = Environment()
# Use the database connection string from the environment variables.
SQLALCHEMY_DATABASE_URL = env.db_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

def get_session():
    """Generate a new database session.
    This session is designed for a single request and will automatically close
    when the response is returned.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()