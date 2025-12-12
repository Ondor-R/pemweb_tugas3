from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:18oktober@localhost:5432/tugas3_db"

engine = create_engine(DATABASE_URL)
DBSession = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

def get_db_session(request):
    return DBSession()