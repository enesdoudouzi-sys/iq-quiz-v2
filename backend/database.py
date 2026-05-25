from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./iqquiz.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Highscore(Base):
    __tablename__ = "highscores"
    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String, index=True)
    iq       = Column(Integer)
    level    = Column(Integer)
    datum    = Column(DateTime, default=datetime.now)

class User(Base):
    __tablename__ = "users"
    id           = Column(Integer, primary_key=True, index=True)
    username     = Column(String, unique=True, index=True)
    email        = Column(String, unique=True, index=True)
    password     = Column(String)
    erstellt_am  = Column(DateTime, default=datetime.now)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
