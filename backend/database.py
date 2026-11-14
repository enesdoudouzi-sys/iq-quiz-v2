from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

import os

# Dauerhafte Datenbank: Auf Render die Umgebungsvariable DATABASE_URL setzen
# (z. B. kostenlose PostgreSQL-Datenbank von Neon oder Supabase).
# Ohne DATABASE_URL wird lokal SQLite benutzt – auf dem kostenlosen
# Render-Plan geht diese Datei bei jedem Neustart verloren.
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "").strip() or "sqlite:///./iqquiz.db"
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    # Manche Anbieter liefern noch das alte Schema, SQLAlchemy 2 braucht postgresql://
    SQLALCHEMY_DATABASE_URL = "postgresql://" + SQLALCHEMY_DATABASE_URL[len("postgres://"):]

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # pool_pre_ping: abgebrochene Verbindungen (z. B. nach Schlafphase) automatisch erneuern
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Highscore(Base):
    __tablename__ = "highscores"
    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String, index=True)
    iq       = Column(Integer)
    level    = Column(Integer)
    datum    = Column(DateTime, default=datetime.now)

class DailyScore(Base):
    __tablename__ = "daily_scores"
    id       = Column(Integer, primary_key=True, index=True)
    datum    = Column(String, index=True)
    name     = Column(String)
    iq       = Column(Integer)
    level    = Column(Integer)
    erstellt = Column(Float)

class User(Base):
    __tablename__ = "users"
    id           = Column(Integer, primary_key=True, index=True)
    username     = Column(String, unique=True, index=True)
    email        = Column(String, unique=True, index=True)
    password     = Column(String)
    erstellt_am  = Column(DateTime, default=datetime.now)

class Ereignis(Base):
    # Anonyme Nutzungs- und Fehlerstatistik: keine IP, kein Name, keine Geräte-ID
    __tablename__ = "ereignisse"
    id       = Column(Integer, primary_key=True, index=True)
    typ      = Column(String, index=True)   # start | ende | fehler
    info     = Column(String)
    datum    = Column(DateTime, default=datetime.now, index=True)

class Kontakt(Base):
    __tablename__ = "kontakt"
    id        = Column(Integer, primary_key=True, index=True)
    name      = Column(String)
    email     = Column(String)
    nachricht = Column(String)
    erstellt  = Column(DateTime, default=datetime.now)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
