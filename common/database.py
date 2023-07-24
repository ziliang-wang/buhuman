from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from app.config.config import config
from app.settings import env


def db_connect():
    engine = create_engine(config[env].db_url, echo=config[env].is_echo, pool_size=10, max_overflow=30)
    session = sessionmaker(engine)
    db_session = scoped_session(session)
    Base = declarative_base()

    return engine, db_session, Base