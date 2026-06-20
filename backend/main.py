from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
import os, random, uuid, time

from fragen import ALLE_FRAGEN, IQ_TABELLE, PREISSTUFEN, SICHERHEITSSTUFEN, IQ_BEZEICHNUNG, get_random_fragen, get_daily_fragen
from database import get_db, create_tables, Highscore, DailyScore
from datetime import date as dt_date

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="IQ Quiz API", docs_url=None, redoc_url=None)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://enesdoudouzi-sys.github.io",
        "https://iq-quiz-v2.onrender.com",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

FRONTEND = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(FRONTEND):
    app.mount("/static", StaticFiles(directory=FRONTEND), name="static")

create_tables()
sessions = {}

SESSION_TTL = 3 * 3600  # 3 Stunden

def cleanup_sessions():
    now = time.time()
    expired = [k for k, v in sessions.items() if now - v.get("erstellt", now) > SESSION_TTL]
    for k in expired:
        del sessions[k]

class StartRequest(BaseModel):
    name: str
    kategorie: str = "alle"
    schwierigkeit: str = "alle"
    @validator('name')
    def name_valid(cls, v):
        v = v.strip()
        if len(v) < 1 or len(v) > 20:
            raise ValueError('Name muss 1-20 Zeichen lang sein')
        return v

class AntwortRequest(BaseModel):
    session_id: str
    level: int
    antwort: str
    @validator('antwort')
    def antwort_valid(cls, v):
        if v.upper() not in ['A','B','C','D','X']:
            raise ValueError('Ungueltige Antwort')
        return v.upper()
    @validator('level')
    def level_valid(cls, v):
        if v < 1 or v > 50:
            raise ValueError('Ungueltiges Level')
        return v

class JokerRequest(BaseModel):
    session_id: str
    level: int
    typ: str
    gesperrte: list = []
    @validator('typ')
    def typ_valid(cls, v):
        if v not in ['5050','telefon','publikum']:
            raise ValueError('Ungueltiger Joker')
        return v

class HighscoreRequest(BaseModel):
    name: str
    iq: int
    level: int
    session_id: str = ""
    @validator('name')
    def name_valid(cls, v):
        return v.strip()[:20]
    @validator('iq')
    def iq_valid(cls, v):
        if v < 0 or v > 200:
            raise ValueError('Ungueltiger IQ')
        return v

class DailySubmitRequest(BaseModel):
    name: str
    iq: int
    level: int
    session_id: str = ""
    @validator('name')
    def name_valid(cls, v):
        return v.strip()[:20]
    @validator('iq')
    def iq_valid(cls, v):
        if v < 0 or v > 200:
            raise ValueError('Ungueltiger IQ')
        return v

def iq_bezeichnung(iq: int) -> str:
    for bereich, bez in IQ_BEZEICHNUNG.items():
        if iq in bereich:
            return bez
    return "Ausnahmetalent"

def get_session(session_id: str):
    if not session_id or session_id not in sessions:
        raise HTTPException(404, "Session nicht gefunden")
    return sessions[session_id]

@app.get("/")
def root():
    index = os.path.join(FRONTEND, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    return {"status": "IQ Quiz API"}

@app.get("/health")
def health():
    return {"status": "ok", "sessions": len(sessions)}

@app.post("/api/start")
@limiter.limit("10/minute")
def start_game(request: Request, req: StartRequest):
    cleanup_sessions()
    if len(sessions) > 1000:
        oldest = list(sessions.keys())[:100]
        for k in oldest:
            del sessions[k]
    session_id = str(uuid.uuid4())
    fragen = get_random_fragen(15, req.kategorie, req.schwierigkeit)
    sessions[session_id] = {
        "name":            req.name,
        "fragen":          fragen,
        "joker":           {"5050": True, "telefon": True, "publikum": True},
        "sicher_level":    0,
        "aktuelles_level": 1,
        "erstellt":        time.time(),
        "final_iq":        85,
        "final_level":     0,
    }
    return {"session_id": session_id, "total": len(fragen)}

@app.get("/api/frage/{session_id}/{level}")
@limiter.limit("60/minute")
def get_frage(request: Request, session_id: str, level: int):
    session = get_session(session_id)
    fragen = session["fragen"]
    frage = next((f for f in fragen if f["level"] == level), None)
    if not frage:
        raise HTTPException(404, "Frage nicht gefunden")
    return {
        "level":          frage["level"],
        "frage":          frage["frage"],
        "antworten":      frage["antworten"],
        "kategorie":      frage["kategorie"],
        "schwierigkeit":  frage.get("schwierigkeit", 1),
        "preis":          PREISSTUFEN.get(level, "1.000.000 EUR"),
        "sicher":         level in SICHERHEITSSTUFEN,
        "seq":            frage.get("seq"),
    }

@app.post("/api/antwort")
@limiter.limit("60/minute")
def pruefe_antwort(request: Request, req: AntwortRequest):
    session = get_session(req.session_id)
    if req.level != session.get("aktuelles_level", 1):
        raise HTTPException(400, "Ungueltige Level-Reihenfolge")
    fragen = session["fragen"]
    frage = next((f for f in fragen if f["level"] == req.level), None)
    if not frage:
        raise HTTPException(404, "Frage nicht gefunden")
    richtig = req.antwort == frage["richtig"]
    if richtig and req.level in SICHERHEITSSTUFEN:
        session["sicher_level"] = req.level
    session["aktuelles_level"] = req.level + 1
    sicher = session["sicher_level"]
    iq_level = req.level if richtig else sicher
    iq = IQ_TABELLE.get(iq_level, 85)
    # Fortschritt im Server tracken für Highscore-Validierung
    session["final_iq"] = iq
    session["final_level"] = req.level if richtig else req.level - 1
    return {
        "richtig":               richtig,
        "richtige_antwort":      frage["richtig"],
        "richtige_antwort_text": frage["antworten"][frage["richtig"]],
        "erklaerung":            frage.get("erklaerung", ""),
        "iq":                    iq,
        "iq_text":               iq_bezeichnung(iq),
        "sicher_level":          sicher,
    }

@app.post("/api/joker")
@limiter.limit("20/minute")
def joker(request: Request, req: JokerRequest):
    session = get_session(req.session_id)
    if not session["joker"].get(req.typ):
        raise HTTPException(400, "Joker bereits verwendet")
    fragen = session["fragen"]
    frage = next((f for f in fragen if f["level"] == req.level), None)
    if not frage:
        raise HTTPException(404, "Frage nicht gefunden")
    richtig = frage["richtig"]
    session["joker"][req.typ] = False
    if req.typ == "5050":
        falsche = [k for k in ["A","B","C","D"] if k != richtig and k not in req.gesperrte]
        entfernen = random.sample(falsche, min(2, len(falsche)))
        return {"typ": "5050", "entfernte": entfernen}
    elif req.typ == "telefon":
        if random.random() < 0.80:
            tipp = richtig
            text = random.choice(["Ich bin mir sicher:", "Ohne Zweifel:", "Ich glaube es ist"])
        else:
            falsche = [k for k in ["A","B","C","D"] if k != richtig]
            tipp = random.choice(falsche)
            text = "Bin nicht sicher, aber..."
        return {"typ": "telefon", "tipp": tipp, "text": text}
    elif req.typ == "publikum":
        verfuegbar = [k for k in ["A","B","C","D"] if k not in req.gesperrte]
        stimmen = {k: random.randint(45,70) if k==richtig else random.randint(5,20) for k in verfuegbar}
        total = sum(stimmen.values())
        stimmen = {k: round(v/total*100) for k,v in stimmen.items()}
        return {"typ": "publikum", "stimmen": stimmen}

@app.post("/api/daily/start")
@limiter.limit("5/minute")
def start_daily(request: Request, req: StartRequest):
    cleanup_sessions()
    if len(sessions) > 1000:
        oldest = list(sessions.keys())[:100]
        for k in oldest:
            del sessions[k]
    today = dt_date.today().isoformat()
    session_id = str(uuid.uuid4())
    fragen = get_daily_fragen(today, 15)
    sessions[session_id] = {
        "name":            req.name,
        "fragen":          fragen,
        "joker":           {"5050": True, "telefon": True, "publikum": True},
        "sicher_level":    0,
        "aktuelles_level": 1,
        "erstellt":        time.time(),
        "daily":           True,
        "datum":           today,
        "daily_submitted": False,
        "final_iq":        85,
        "final_level":     0,
    }
    return {"session_id": session_id, "total": 15, "datum": today}

@app.get("/api/daily/highscores")
@limiter.limit("30/minute")
def get_daily_highscores(request: Request, db: Session = Depends(get_db)):
    today = dt_date.today().isoformat()
    scores = db.query(DailyScore).filter(DailyScore.datum == today).order_by(DailyScore.iq.desc()).limit(10).all()
    return [{"name": s.name, "iq": s.iq, "level": s.level} for s in scores]

@app.post("/api/daily/submit")
@limiter.limit("3/minute")
def submit_daily(request: Request, req: DailySubmitRequest, db: Session = Depends(get_db)):
    today = dt_date.today().isoformat()
    # Doppeleinreichung über Session verhindern
    if req.session_id and req.session_id in sessions:
        session = sessions[req.session_id]
        if session.get("daily_submitted"):
            raise HTTPException(400, "Bereits heute eingereicht")
        session["daily_submitted"] = True
        # IQ aus Session nehmen statt Client-Wert zu vertrauen
        verified_iq = session.get("final_iq", req.iq)
        verified_level = session.get("final_level", req.level)
    else:
        verified_iq = req.iq
        verified_level = req.level
    score = DailyScore(datum=today, name=req.name, iq=verified_iq, level=verified_level, erstellt=time.time())
    db.add(score)
    db.commit()
    return {"ok": True}

@app.get("/api/offline")
@limiter.limit("10/minute")
def get_offline_fragen(request: Request):
    fragen = get_random_fragen(15)
    return [{"level": f["level"], "frage": f["frage"], "antworten": f["antworten"],
             "richtig": f["richtig"], "kategorie": f["kategorie"],
             "schwierigkeit": f.get("schwierigkeit", 1),
             "seq": f.get("seq"), "erklaerung": f.get("erklaerung", "")} for f in fragen]

@app.get("/api/highscores")
@limiter.limit("30/minute")
def get_highscores(request: Request, db: Session = Depends(get_db)):
    scores = db.query(Highscore).order_by(Highscore.iq.desc()).limit(10).all()
    return [{"name": s.name, "iq": s.iq, "level": s.level} for s in scores]

@app.post("/api/highscores")
@limiter.limit("5/minute")
def post_highscore(request: Request, req: HighscoreRequest, db: Session = Depends(get_db)):
    # IQ aus Session validieren wenn session_id mitgeschickt wird
    if req.session_id and req.session_id in sessions:
        session = sessions[req.session_id]
        verified_iq = session.get("final_iq", req.iq)
        verified_level = session.get("final_level", req.level)
    else:
        # Ohne Session: Plausibilitätsprüfung
        verified_iq = min(req.iq, 145)
        verified_level = min(req.level, 15)
    score = Highscore(name=req.name, iq=verified_iq, level=verified_level)
    db.add(score)
    db.commit()
    return {"ok": True}
