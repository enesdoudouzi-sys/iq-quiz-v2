from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
import os, random, uuid, time, re, hmac

from fragen import ALLE_FRAGEN, IQ_TABELLE, PREISSTUFEN, SICHERHEITSSTUFEN, IQ_BEZEICHNUNG, get_random_fragen, get_daily_fragen
from database import get_db, create_tables, Highscore, DailyScore, Kontakt
from datetime import date as dt_date

def client_ip(request: Request) -> str:
    # Render (und andere Hoster) setzen die echte Nutzer-IP in X-Forwarded-For.
    # Ohne das teilen sich alle Nutzer das Limit der Proxy-IP.
    fwd = request.headers.get("x-forwarded-for", "")
    return fwd.split(",")[0].strip() or get_remote_address(request)

limiter = Limiter(key_func=client_ip)
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
        "https://localhost",  # Android-App (Capacitor, androidScheme https)
        "https://html-classic.itch.zone",  # itch.io (Spiel laeuft dort im iframe)
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

# Namen in der öffentlichen Bestenliste: nur druckbare Zeichen, Länge 1-20,
# einfacher Filter gegen Beleidigungen (Google-Play-Richtlinie für Nutzerinhalte).
_BLOCKED = ["nazi","hitler","fick","fuck","hure","nutte","fotze","wichser","arschloch","schlampe","bitch","cunt","nigger","nigga","neger","kanake","schwuchtel","faggot","retard","porn","sex","penis","vagina","orospu","siktir","amk","piç","kahpe","yarrak","göt"]
def clean_name(v: str) -> str:
    v = re.sub(r"[\x00-\x1f\x7f<>]", "", (v or "")).strip()[:20]
    if not v:
        raise ValueError('Name fehlt')
    norm = re.sub(r"[^a-zäöüßçğış]", "", v.lower().replace("0","o").replace("1","i").replace("3","e").replace("4","a").replace("5","s").replace("@","a").replace("$","s"))
    if any(b in norm for b in _BLOCKED):
        raise ValueError('Name nicht erlaubt')
    return v

class StartRequest(BaseModel):
    name: str
    kategorie: str = "alle"
    schwierigkeit: str = "alle"
    @validator('name')
    def name_valid(cls, v):
        v = v.strip()
        if len(v) < 1 or len(v) > 20:
            raise ValueError('Name muss 1-20 Zeichen lang sein')
        return clean_name(v)

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

class KontaktRequest(BaseModel):
    name: str
    email: str
    nachricht: str
    website: str = ""  # Honeypot, muss leer bleiben
    @validator('name')
    def name_valid(cls, v):
        v = v.strip()
        if len(v) < 1 or len(v) > 100:
            raise ValueError('Name muss 1-100 Zeichen lang sein')
        return v
    @validator('email')
    def email_valid(cls, v):
        v = v.strip()
        if len(v) > 200 or not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', v):
            raise ValueError('Ungueltige E-Mail-Adresse')
        return v
    @validator('nachricht')
    def nachricht_valid(cls, v):
        v = v.strip()
        if len(v) < 5 or len(v) > 3000:
            raise ValueError('Nachricht muss 5-3000 Zeichen lang sein')
        return v

class JokerRequest(BaseModel):
    session_id: str
    level: int
    typ: str
    gesperrte: list = []
    @validator('typ')
    def typ_valid(cls, v):
        if v not in ['5050','telefon','publikum','skip','doppel']:
            raise ValueError('Ungueltiger Joker')
        return v

class HighscoreRequest(BaseModel):
    name: str
    iq: int
    level: int
    session_id: str = ""
    @validator('name')
    def name_valid(cls, v):
        return clean_name(v)
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
        return clean_name(v)
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
        "joker":           {"5050": True, "telefon": True, "publikum": True, "skip": True, "doppel": True},
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
    if not richtig and session.get("doppel_level") == req.level:
        # Doppel-Chance: zweiter Versuch, Level bleibt, Lösung wird nicht verraten
        session.pop("doppel_level", None)
        return {"richtig": False, "zweiter_versuch": True}
    session.pop("doppel_level", None)
    if richtig and req.level in SICHERHEITSSTUFEN:
        session["sicher_level"] = req.level
    session["aktuelles_level"] = req.level + 1
    sicher = session["sicher_level"]
    iq_level = req.level if richtig else sicher
    iq = IQ_TABELLE.get(iq_level, 85)
    # Fortschritt für die Highscore-Prüfung: nach der ersten falschen Antwort
    # wird das Ergebnis eingefroren (Lern-/Time-Attack-Modus spielen weiter,
    # dürfen den Bestenlisten-Wert aber nicht mehr erhöhen)
    if not session.get("eingefroren"):
        session["final_iq"] = iq
        session["final_level"] = req.level if richtig else req.level - 1
        if not richtig:
            session["eingefroren"] = True
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
    if req.typ in ("skip", "doppel") and req.level != session.get("aktuelles_level", 1):
        raise HTTPException(400, "Ungueltige Level-Reihenfolge")
    session["joker"][req.typ] = False
    if req.typ == "skip":
        # Frage überspringen: weiter zum nächsten Level, IQ bleibt unverändert
        session["aktuelles_level"] = req.level + 1
        return {"typ": "skip"}
    if req.typ == "doppel":
        session["doppel_level"] = req.level
        return {"typ": "doppel"}
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
        "joker":           {"5050": True, "telefon": True, "publikum": True, "skip": True, "doppel": True},
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
    session = sessions.get(req.session_id) if req.session_id else None
    if not session:
        raise HTTPException(400, "Ungueltige oder abgelaufene Spiel-Session")
    if session.get("daily_submitted"):
        raise HTTPException(400, "Bereits heute eingereicht")
    session["daily_submitted"] = True
    # IQ aus der Session statt dem Client-Wert vertrauen
    verified_iq = session.get("final_iq", 85)
    verified_level = session.get("final_level", 0)
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
    # Nur Ergebnisse aus einem echten Spiel auf diesem Server zählen (kein freies Eintragen)
    session = sessions.get(req.session_id) if req.session_id else None
    if not session:
        raise HTTPException(400, "Ungueltige oder abgelaufene Spiel-Session")
    if session.get("hs_submitted"):
        raise HTTPException(400, "Bereits gespeichert")
    session["hs_submitted"] = True
    verified_iq = session.get("final_iq", 85)
    verified_level = session.get("final_level", 0)
    score = Highscore(name=req.name, iq=verified_iq, level=verified_level)
    db.add(score)
    db.commit()
    return {"ok": True}

@app.post("/api/kontakt")
@limiter.limit("3/minute")
def kontakt(request: Request, req: KontaktRequest, db: Session = Depends(get_db)):
    if req.website:
        return {"ok": True}  # Bot: still verwerfen
    db.add(Kontakt(name=req.name, email=req.email, nachricht=req.nachricht))
    db.commit()
    return {"ok": True}

@app.get("/api/kontakt")
@limiter.limit("10/minute")
def kontakt_liste(request: Request, db: Session = Depends(get_db)):
    # Nur fuer den Betreiber: Header "X-Admin-Token" = Umgebungsvariable ADMIN_TOKEN (auf Render setzen)
    token = os.environ.get("ADMIN_TOKEN", "")
    if not token or not hmac.compare_digest(request.headers.get("X-Admin-Token", ""), token):
        raise HTTPException(status_code=403, detail="Kein Zugriff")
    rows = db.query(Kontakt).order_by(Kontakt.erstellt.desc()).limit(100).all()
    return [{"id": k.id, "name": k.name, "email": k.email, "nachricht": k.nachricht,
             "erstellt": k.erstellt.isoformat()} for k in rows]
