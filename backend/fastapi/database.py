from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://dbmasteruser:dbmaster@ls-644e915cc7a6ba69ccf824a69cef04d45c847ed5.cps8g04q216q.ap-northeast-1.rds.amazonaws.com:5432/micropost?sslmode=require"
engine = create_engine(DATABASE_URL)
