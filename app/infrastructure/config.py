from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings


def get_engine():
    return create_engine(settings.DATABASE_URI)


def get_session():
    engine = get_engine()
    return sessionmaker(bind=engine)
