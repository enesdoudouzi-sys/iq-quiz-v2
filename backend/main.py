from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os, random, uuid

from fragen import ALLE_FRAGEN, IQ_TABELLE, PREISSTUFEN, SICHERHEITSSTUFEN, IQ_BEZEICHNUNG, get_random_fragen
from database import get_db, create_tables, Highscore

app = FastAPI(title="IQ Quiz API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")

create_tables()
sessions = {}

class StartRequest(BaseModel):
    name: str

class AntwortRequest(BaseModel):
    session_id: str
    level: int
    antwort: str

class JokerRequest(BaseModel):
    session_id: str
    level: int
    typ: str
    gesperrte: list = []

class HighscoreRequest(BaseModel):
    name: str
    iq: int
    level: int

def iq_bezeichnung(iq: int) -> str:
    for bereich, bez in IQ_BEZEICHNUNG.items():
        if iq in bereich:
            return bez
    return "Ausnahmetalent"

@app.get("/")
def root():
    return FileResponse(os.path.join(FRONTEND, "index.html"))

@app.post("/api/start")
def start_game(req: StartRequest):
    session_id = str(uuid.uuid4())
    fragen = get_random_fragen(50)
    sessions[session_id] = {
        "name": req.name,
        "fragen": fragen,
        "joker": {"5050": True, "telefon": True, "publikum": True},
        "sicher_level": 0,
    }
    return {"session_id": session_id, "total": len(fragen)}

@app.get("/api/frage/{session_id}/{level}")
def get_frage(session_id: str, level: int):
    if session_id not in sessions:
        raise HTTPException(404, "Session nicht gefunden")
    fragen = sessions[session_id]["fragen"]
    frage = next((f for f in fragen if f["level"] == level), None)
    if not frage:
        raise HTTPException(404, "Frage nicht gefunden")
    return {
        "level":     frage["level"],
        "frage":     frage["frage"],
        "antworten": frage["antworten"],
        "kategorie": frage["kategorie"],
        "preis":     PREISSTUFEN.get(level, "1.000.000 EUR"),
        "sicher":    level in SICHERHEITSSTUFEN,
        "seq":       frage.get("seq"),
        "richtig":   frage["richtig"],
    }

@app.post("/api/antwort")
def pruefe_antwort(req: AntwortRequest):
    if req.session_id not in sessions:
        raise HTTPException(404, "Session nicht gefunden")
    session = sessions[req.session_id]
    fragen = session["fragen"]
    frage = next((f for f in fragen if f["level"] == req.level), None)
    if not frage:
        raise HTTPException(404, "Frage nicht gefunden")
    richtig = req.antwort.upper() == frage["richtig"]
    if richtig and req.level in SICHERHEITSSTUFEN:
        session["sicher_level"] = req.level
    sicher = session["sicher_level"]
    iq_level = req.level if richtig else sicher
    iq = IQ_TABELLE.get(iq_level, 85)
    return {
        "richtig":               richtig,
        "richtige_antwort":      frage["richtig"],
        "richtige_antwort_text": frage["antworten"][frage["richtig"]],
        "iq":                    iq,
        "iq_text":               iq_bezeichnung(iq),
        "sicher_level":          sicher,
    }

@app.post("/api/joker")
def joker(req: JokerRequest):
    if req.session_id not in sessions:
        raise HTTPException(404, "Session nicht gefunden")
    session = sessions[req.session_id]
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
            text = random.choice(["Ich bin mir sicher, es ist","Ohne zu zoegern:","Ich glaube es ist"])
        else:
            falsche = [k for k in ["A","B","C","D"] if k != richtig]
            tipp = random.choice(falsche)
            text = "Bin nicht sicher, aber ich glaube..."
        return {"typ": "telefon", "tipp": tipp, "text": text}
    elif req.typ == "publikum":
        verfuegbar = [k for k in ["A","B","C","D"] if k not in req.gesperrte]
        stimmen = {}
        for k in verfuegbar:
            stimmen[k] = random.randint(45,70) if k==richtig else random.randint(5,20)
        total = sum(stimmen.values())
        stimmen = {k: round(v/total*100) for k,v in stimmen.items()}
        return {"typ": "publikum", "stimmen": stimmen}
    raise HTTPException(400, "Unbekannter Joker")

@app.get("/api/highscores")
def get_highscores(db: Session = Depends(get_db)):
    scores = db.query(Highscore).order_by(Highscore.iq.desc()).limit(10).all()
    return [{"name": s.name, "iq": s.iq, "level": s.level} for s in scores]

@app.post("/api/highscores")
def post_highscore(req: HighscoreRequest, db: Session = Depends(get_db)):
    score = Highscore(name=req.name, iq=req.iq, level=req.level)
    db.add(score)
    db.commit()
    return {"ok": True}

@app.get("/health")
def health():
    return {"status": "ok"}
