from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from env import Environment

env = Environment()
# For SQLite, no need for user/password/host/port so we use a file based DB.
SQLALCHEMY_DATABASE_URL = "sqlite:///./mydatabase.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
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