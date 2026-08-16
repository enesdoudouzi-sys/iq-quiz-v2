import os
import secrets
import warnings
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db, User

# JWT-Secret MUSS über eine Umgebungsvariable gesetzt werden (z.B. im Render
# Dashboard unter Environment). Frueher stand hier ein fest einprogrammierter,
# oeffentlich im Git-Repo sichtbarer Schluessel - das ist ein Sicherheitsrisiko,
# da damit jeder gueltige Login-Tokens faelschen konnte.
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not SECRET_KEY:
    warnings.warn(
        "JWT_SECRET_KEY ist nicht gesetzt! Es wird ein zufaelliger Schluessel "
        "nur fuer diesen Prozess generiert - alle bestehenden Tokens werden "
        "damit ungueltig, sobald der Server neu startet. Bitte JWT_SECRET_KEY "
        "als Umgebungsvariable in Render setzen (z.B. via `openssl rand -hex 32`).",
        RuntimeWarning,
    )
    SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 Tage

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def hash_password(password):
    return pwd_context.hash(password)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            return None
        user = db.query(User).filter(User.username == username).first()
        return user
    except JWTError:
        return None
