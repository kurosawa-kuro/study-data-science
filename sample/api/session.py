from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from env import Environment

env = Environment()
# PostgreSQLの接続URL
SQLALCHEMY_DATABASE_URL = "postgresql://dbmasteruser:dbmaster@ls-644e915cc7a6ba69ccf824a69cef04d45c847ed5.cps8g04q216q.ap-northeast-1.rds.amazonaws.com:5432/dbmaster?sslmode=require"
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