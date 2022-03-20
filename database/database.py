from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from database.config import setting

engine = create_engine(setting.DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
