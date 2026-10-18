from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
import os, random, re, uuid, time
from collections import defaultdict, deque

from fragen import ALLE_FRAGEN, IQ_TABELLE, PREISSTUFEN, SICHERHEITSSTUFEN, IQ_BEZEICHNUNG, get_random_fragen, get_daily_fragen
from database import get_db, create_tables, Highscore, DailyScore
from datetime import date as dt_date

# ── Konfiguration ──────────────────────────────────────────────────────────
# Anzahl vertrauenswuerdiger Proxys vor dem Server (Render = 1). Bestimmt, welcher
# Eintrag aus X-Forwarded-For als Client-IP gilt. 0 = Header ignorieren.
TRUSTED_PROXY_HOPS = int(os.environ.get("TRUSTED_PROXY_HOPS", "1"))

DEFAULT_ORIGINS = [
    "https://enesdoudouzi-sys.github.io",   # Web-Version
    "https://iq-quiz-v2.onrender.com",
    "https://localhost",                    # Android-App (Capacitor, androidScheme=https)
    "capacitor://localhost",                # iOS-App
]
ALLOWED_ORIGINS = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", ",".join(DEFAULT_ORIGINS)).split(",") if o.strip()]
if os.environ.get("DEV_MODE") == "1":
    ALLOWED_ORIGINS += ["http://localhost:8000", "http://127.0.0.1:8000", "http://127.0.0.1:8765", "http://localhost:8765"]

SESSION_TTL = 2 * 3600            # Sekunden
MAX_SESSIONS = 5000               # global
MAX_SESSIONS_PER_IP = 30          # pro IP (aeltere eigene Sessions werden verdraengt)
MIN_ANTWORT_SEKUNDEN = 0.7        # schneller kann kein Mensch lesen und antworten
MAX_EINREICHUNGEN_PRO_STUNDE = 20 # Highscore-Eintraege pro IP
MAX_BODY_BYTES = 10_000

MODI = {"normal", "timeattack", "learn", "endless"}
BESTENLISTEN_MODI = {"normal", "endless", "daily"}   # nur hier zaehlt das Ergebnis
KATEGORIEN = {"alle"} | {f["kategorie"] for f in ALLE_FRAGEN}
SCHWIERIGKEITEN = {"alle", "1", "2", "3"}
BUCHSTABEN = ("A", "B", "C", "D")


def client_ip(request: Request) -> str:
    """Client-IP hinter Proxy (Render). Spoofing-sicher: es zaehlt der Eintrag,
    den der eigene vertrauenswuerdige Proxy angehaengt hat (von rechts gezaehlt)."""
    if TRUSTED_PROXY_HOPS > 0:
        xff = request.headers.get("x-forwarded-for", "")
        teile = [t.strip() for t in xff.split(",") if t.strip()]
        if len(teile) >= TRUSTED_PROXY_HOPS:
            return teile[-TRUSTED_PROXY_HOPS][:64]
    return request.client.host if request.client else "unbekannt"


limiter = Limiter(key_func=client_ip)
app = FastAPI(title="IQ Quiz API", docs_url=None, redoc_url=None, openapi_url=None)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.middleware("http")
async def sicherheit(request: Request, call_next):
    laenge = request.headers.get("content-length")
    if laenge and laenge.isdigit() and int(laenge) > MAX_BODY_BYTES:
        return JSONResponse({"detail": "Anfrage zu gross"}, status_code=413)
    antwort = await call_next(request)
    antwort.headers["X-Content-Type-Options"] = "nosniff"
    antwort.headers["X-Frame-Options"] = "DENY"
    antwort.headers["Referrer-Policy"] = "no-referrer"
    antwort.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    if request.url.path.startswith("/api/"):
        antwort.headers["Cache-Control"] = "no-store"
    return antwort


FRONTEND = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(FRONTEND):
    app.mount("/static", StaticFiles(directory=FRONTEND), name="static")

create_tables()
sessions = {}
_einreichungen = defaultdict(deque)


# ── Hilfsfunktionen ────────────────────────────────────────────────────────
_STEUERZEICHEN = re.compile(r"[\x00-\x1f\x7f<>]")


def bereinige_name(v: str) -> str:
    v = _STEUERZEICHEN.sub("", v or "")
    v = " ".join(v.split())[:20].strip()
    if not v:
        raise ValueError("Name muss 1-20 Zeichen lang sein")
    return v


def cleanup_sessions():
    jetzt = time.time()
    abgelaufen = [k for k, v in sessions.items() if jetzt - v.get("erstellt", jetzt) > SESSION_TTL]
    for k in abgelaufen:
        del sessions[k]


def neue_session(ip: str, **felder) -> str:
    """Legt eine Session an. Eine einzelne IP kann nur ihre eigenen aelteren
    Sessions verdraengen, nie die anderer Spieler."""
    cleanup_sessions()
    eigene = sorted((k for k, v in sessions.items() if v.get("ip") == ip), key=lambda k: sessions[k]["erstellt"])
    for k in eigene[: max(0, len(eigene) - MAX_SESSIONS_PER_IP + 1)]:
        del sessions[k]
    if len(sessions) >= MAX_SESSIONS:
        raise HTTPException(503, "Server ausgelastet, bitte spaeter erneut versuchen")
    sid = str(uuid.uuid4())
    sessions[sid] = {
        "ip": ip,
        "erstellt": time.time(),
        "joker": {"5050": True, "telefon": True, "publikum": True, "skip": True, "doppel": True},
        "sicher_level": 0,
        "aktuelles_level": 1,
        "final_iq": 85,
        "final_level": 0,
        "finished": False,
        "submitted": False,
        **felder,
    }
    return sid


def pruefe_einreichungs_limit(ip: str):
    jetzt = time.time()
    q = _einreichungen[ip]
    while q and jetzt - q[0] > 3600:
        q.popleft()
    if len(q) >= MAX_EINREICHUNGEN_PRO_STUNDE:
        raise HTTPException(429, "Zu viele Eintraege, bitte spaeter erneut versuchen")
    q.append(jetzt)
    if len(_einreichungen) > 10000:
        for k in [k for k, d in _einreichungen.items() if not d]:
            del _einreichungen[k]


def beendete_session(session_id: str, daily: bool) -> dict:
    """Eine Bestenlisten-Einreichung ist nur fuer eine beendete, noch nicht
    eingereichte Session des passenden Typs gueltig. Die Werte kommen vom Server."""
    s = sessions.get(session_id)
    if not s:
        raise HTTPException(400, "Ungueltige oder abgelaufene Sitzung")
    if s["submitted"]:
        raise HTTPException(400, "Ergebnis wurde bereits eingereicht")
    if bool(s.get("daily")) != daily:
        raise HTTPException(400, "Falscher Spieltyp")
    if s.get("modus") not in BESTENLISTEN_MODI:
        raise HTTPException(400, "Fuer diesen Modus gibt es keine Bestenliste")
    if not s["finished"]:
        raise HTTPException(400, "Das Spiel ist noch nicht beendet")
    if daily and s.get("datum") != dt_date.today().isoformat():
        raise HTTPException(400, "Die Tages-Challenge ist abgelaufen")
    return s


def get_session(session_id: str):
    if not session_id or session_id not in sessions:
        raise HTTPException(404, "Session nicht gefunden")
    return sessions[session_id]


def iq_bezeichnung(iq: int) -> str:
    for bereich, bez in IQ_BEZEICHNUNG.items():
        if iq in bereich:
            return bez
    return "Ausnahmetalent"


# ── Anfrage-Modelle ────────────────────────────────────────────────────────
class StartRequest(BaseModel):
    name: str
    kategorie: str = "alle"
    schwierigkeit: str = "alle"
    modus: str = "normal"

    @field_validator("name")
    @classmethod
    def name_valid(cls, v):
        return bereinige_name(v)

    @field_validator("kategorie")
    @classmethod
    def kategorie_valid(cls, v):
        if v not in KATEGORIEN:
            raise ValueError("Unbekannte Kategorie")
        return v

    @field_validator("schwierigkeit")
    @classmethod
    def schwierigkeit_valid(cls, v):
        if v not in SCHWIERIGKEITEN:
            raise ValueError("Unbekannte Schwierigkeit")
        return v

    @field_validator("modus")
    @classmethod
    def modus_valid(cls, v):
        if v not in MODI:
            raise ValueError("Unbekannter Modus")
        return v


class AntwortRequest(BaseModel):
    session_id: str
    level: int
    antwort: str

    @field_validator("session_id")
    @classmethod
    def sid_valid(cls, v):
        if len(v) > 64:
            raise ValueError("Ungueltige Session")
        return v

    @field_validator("antwort")
    @classmethod
    def antwort_valid(cls, v):
        if v.upper() not in ["A", "B", "C", "D", "X"]:
            raise ValueError("Ungueltige Antwort")
        return v.upper()

    @field_validator("level")
    @classmethod
    def level_valid(cls, v):
        if v < 1 or v > 50:
            raise ValueError("Ungueltiges Level")
        return v


class JokerRequest(BaseModel):
    session_id: str
    level: int
    typ: str
    gesperrte: list[str] = []

    @field_validator("session_id")
    @classmethod
    def sid_valid(cls, v):
        if len(v) > 64:
            raise ValueError("Ungueltige Session")
        return v

    @field_validator("typ")
    @classmethod
    def typ_valid(cls, v):
        if v not in ["5050", "telefon", "publikum", "skip", "doppel"]:
            raise ValueError("Ungueltiger Joker")
        return v

    @field_validator("gesperrte")
    @classmethod
    def gesperrte_valid(cls, v):
        v = [x.upper() for x in v if isinstance(x, str)]
        if len(v) > 4 or any(x not in BUCHSTABEN for x in v):
            raise ValueError("Ungueltige Auswahl")
        return v


class EinreichungRequest(BaseModel):
    """Bestenliste/Tages-Challenge. iq und level werden nur noch aus
    Kompatibilitaetsgruenden angenommen; gespeichert werden Serverwerte."""
    name: str
    iq: int = 0
    level: int = 0
    session_id: str

    @field_validator("name")
    @classmethod
    def name_valid(cls, v):
        return bereinige_name(v)

    @field_validator("session_id")
    @classmethod
    def sid_valid(cls, v):
        if not v or len(v) > 64:
            raise ValueError("Ungueltige Session")
        return v


# ── Endpunkte ──────────────────────────────────────────────────────────────
@app.get("/")
def root():
    index = os.path.join(FRONTEND, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    return {"status": "IQ Quiz API"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/ip")
@limiter.limit("20/minute")
def meine_ip(request: Request):
    """Diagnose: zeigt, welche Client-IP der Server aus den Proxy-Headern ableitet."""
    return {"ip": client_ip(request)}


@app.post("/api/start")
@limiter.limit("10/minute")
def start_game(request: Request, req: StartRequest):
    fragen = get_random_fragen(15, req.kategorie, req.schwierigkeit)
    sid = neue_session(client_ip(request), name=req.name, fragen=fragen, modus=req.modus)
    return {"session_id": sid, "total": len(fragen)}


@app.get("/api/frage/{session_id}/{level}")
@limiter.limit("60/minute")
def get_frage(request: Request, session_id: str, level: int):
    session = get_session(session_id)
    if level > session["aktuelles_level"]:
        raise HTTPException(400, "Ungueltige Level-Reihenfolge")
    fragen = session["fragen"]
    frage = next((f for f in fragen if f["level"] == level), None)
    if not frage:
        raise HTTPException(404, "Frage nicht gefunden")
    if level == session["aktuelles_level"]:
        session["frage_level"] = level
        session["frage_ts"] = time.time()
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
    if session["finished"]:
        raise HTTPException(400, "Das Spiel ist bereits beendet")
    if req.level != session["aktuelles_level"]:
        raise HTTPException(400, "Ungueltige Level-Reihenfolge")
    if session.get("frage_level") != req.level:
        raise HTTPException(400, "Frage wurde nicht abgerufen")
    # Zeitlimit nach unten: Bots, die Antworten sofort senden, werden abgewiesen
    if req.antwort != "X" and time.time() - session.get("frage_ts", 0) < MIN_ANTWORT_SEKUNDEN:
        raise HTTPException(429, "Zu schnell")
    fragen = session["fragen"]
    frage = next((f for f in fragen if f["level"] == req.level), None)
    if not frage:
        raise HTTPException(404, "Frage nicht gefunden")
    richtig = req.antwort == frage["richtig"]

    # Doppel-Chance: erster Fehlversuch zaehlt nicht, die richtige Antwort wird nicht verraten
    if (not richtig and req.antwort != "X"
            and session.get("doppel_level") == req.level and not session.get("doppel_verbraucht")):
        session["doppel_verbraucht"] = True
        return {"richtig": False, "nochmal": True}

    if richtig and req.level in SICHERHEITSSTUFEN:
        session["sicher_level"] = req.level
    session["aktuelles_level"] = req.level + 1
    sicher = session["sicher_level"]
    iq_level = req.level if richtig else sicher
    iq = IQ_TABELLE.get(iq_level, 85)
    session["final_iq"] = iq
    session["final_level"] = req.level if richtig else req.level - 1
    endet_bei_fehler = session.get("modus") in BESTENLISTEN_MODI
    if req.level >= len(fragen) or (not richtig and endet_bei_fehler):
        session["finished"] = True
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
    if session["finished"]:
        raise HTTPException(400, "Das Spiel ist bereits beendet")
    if req.level != session["aktuelles_level"]:
        raise HTTPException(400, "Ungueltige Level-Reihenfolge")
    if not session["joker"].get(req.typ):
        raise HTTPException(400, "Joker bereits verwendet")
    fragen = session["fragen"]
    frage = next((f for f in fragen if f["level"] == req.level), None)
    if not frage:
        raise HTTPException(404, "Frage nicht gefunden")

    if req.typ == "skip":
        if req.level >= len(fragen):
            raise HTTPException(400, "Die letzte Frage kann nicht uebersprungen werden")
        session["joker"]["skip"] = False
        session["aktuelles_level"] = req.level + 1
        return {"typ": "skip"}
    if req.typ == "doppel":
        session["joker"]["doppel"] = False
        session["doppel_level"] = req.level
        return {"typ": "doppel"}

    richtig = frage["richtig"]
    session["joker"][req.typ] = False
    if req.typ == "5050":
        falsche = [k for k in BUCHSTABEN if k != richtig and k not in req.gesperrte]
        entfernen = random.sample(falsche, min(2, len(falsche)))
        return {"typ": "5050", "entfernte": entfernen}
    elif req.typ == "telefon":
        if random.random() < 0.80:
            tipp = richtig
            text = random.choice(["Ich bin mir sicher:", "Ohne Zweifel:", "Ich glaube es ist"])
        else:
            falsche = [k for k in BUCHSTABEN if k != richtig]
            tipp = random.choice(falsche)
            text = "Bin nicht sicher, aber..."
        return {"typ": "telefon", "tipp": tipp, "text": text}
    else:  # publikum
        verfuegbar = [k for k in BUCHSTABEN if k not in req.gesperrte]
        stimmen = {k: random.randint(45, 70) if k == richtig else random.randint(5, 20) for k in verfuegbar}
        total = sum(stimmen.values())
        stimmen = {k: round(v / total * 100) for k, v in stimmen.items()}
        return {"typ": "publikum", "stimmen": stimmen}


@app.post("/api/daily/start")
@limiter.limit("5/minute")
def start_daily(request: Request, req: StartRequest):
    heute = dt_date.today().isoformat()
    fragen = get_daily_fragen(heute, 15)
    sid = neue_session(client_ip(request), name=req.name, fragen=fragen, modus="daily", daily=True, datum=heute)
    return {"session_id": sid, "total": 15, "datum": heute}


@app.get("/api/daily/highscores")
@limiter.limit("30/minute")
def get_daily_highscores(request: Request, db: Session = Depends(get_db)):
    heute = dt_date.today().isoformat()
    scores = db.query(DailyScore).filter(DailyScore.datum == heute).order_by(DailyScore.iq.desc()).limit(10).all()
    return [{"name": s.name, "iq": s.iq, "level": s.level} for s in scores]


@app.post("/api/daily/submit")
@limiter.limit("3/minute")
def submit_daily(request: Request, req: EinreichungRequest, db: Session = Depends(get_db)):
    ip = client_ip(request)
    session = beendete_session(req.session_id, daily=True)
    pruefe_einreichungs_limit(ip)
    session["submitted"] = True
    heute = dt_date.today().isoformat()
    iq, level = session["final_iq"], session["final_level"]
    # Pro Name und Tag zaehlt nur das beste Ergebnis (verhindert Mehrfach-Eintraege)
    vorhanden = db.query(DailyScore).filter(DailyScore.datum == heute, DailyScore.name == req.name).first()
    if vorhanden:
        if iq > vorhanden.iq:
            vorhanden.iq, vorhanden.level, vorhanden.erstellt = iq, level, time.time()
            db.commit()
    else:
        db.add(DailyScore(datum=heute, name=req.name, iq=iq, level=level, erstellt=time.time()))
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
def post_highscore(request: Request, req: EinreichungRequest, db: Session = Depends(get_db)):
    ip = client_ip(request)
    session = beendete_session(req.session_id, daily=False)
    pruefe_einreichungs_limit(ip)
    session["submitted"] = True
    db.add(Highscore(name=req.name, iq=session["final_iq"], level=session["final_level"]))
    db.commit()
    return {"ok": True}
