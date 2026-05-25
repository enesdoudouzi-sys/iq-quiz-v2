from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json, os, random

from fragen import FRAGEN, IQ_TABELLE, PREISSTUFEN, SICHERHEITSSTUFEN, IQ_BEZEICHNUNG

app = FastAPI(title="IQ Quiz API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")
HIGHSCORE_DATEI = os.path.join(os.path.dirname(__file__), "highscores.json")

class AntwortRequest(BaseModel):
    level: int
    antwort: str

class HighscoreRequest(BaseModel):
    name: str
    iq: int
    level: int

def lade_highscores():
    if os.path.exists(HIGHSCORE_DATEI):
        with open(HIGHSCORE_DATEI) as f:
            return json.load(f)
    return []

def speichere_highscore(name, iq, level):
    scores = lade_highscores()
    scores.append({"name": name, "iq": iq, "level": level})
    scores.sort(key=lambda x: x["iq"], reverse=True)
    with open(HIGHSCORE_DATEI, "w") as f:
        json.dump(scores[:10], f, indent=2)

def iq_bezeichnung(iq: int) -> str:
    for bereich, bez in IQ_BEZEICHNUNG.items():
        if iq in bereich:
            return bez
    return "Außergewöhnlich"

@app.get("/")
def root():
    return FileResponse(os.path.join(FRONTEND, "index.html"))

@app.get("/api/frage/{level}")
def get_frage(level: int):
    frage = next((f for f in FRAGEN if f["level"] == level), None)
    if not frage:
        raise HTTPException(404, "Frage nicht gefunden")
    return {
        "level":               frage["level"],
        "frage":               frage["frage"],
        "antworten":           frage["antworten"],
        "kategorie":           frage["kategorie"],
        "preis":               PREISSTUFEN[level],
        "ist_sicherheitsstufe":level in SICHERHEITSSTUFEN,
        "seq":                 frage.get("seq", None),
    }

@app.post("/api/antwort")
def pruefe_antwort(req: AntwortRequest):
    frage = next((f for f in FRAGEN if f["level"] == req.level), None)
    if not frage:
        raise HTTPException(404, "Frage nicht gefunden")
    richtig      = req.antwort.upper() == frage["richtig"]
    sicher_level = max([s for s in SICHERHEITSSTUFEN if s <= req.level], default=0)
    iq_level     = req.level if richtig else sicher_level
    return {
        "richtig":               richtig,
        "richtige_antwort":      frage["richtig"],
        "richtige_antwort_text": frage["antworten"][frage["richtig"]],
        "naechstes_level":       req.level + 1 if richtig and req.level < 15 else None,
        "gewonnen":              richtig and req.level == 15,
        "iq":                    IQ_TABELLE.get(iq_level, 85),
        "iq_text":               iq_bezeichnung(IQ_TABELLE.get(iq_level, 85)),
    }

@app.get("/api/highscores")
def get_highscores():
    return lade_highscores()

@app.post("/api/highscores")
def post_highscore(req: HighscoreRequest):
    speichere_highscore(req.name, req.iq, req.level)
    return {"ok": True}

@app.get("/api/leiter")
def get_leiter():
    return [
        {"level": lvl, "preis": PREISSTUFEN[lvl], "iq": IQ_TABELLE[lvl], "sicher": lvl in SICHERHEITSSTUFEN}
        for lvl in range(1, 16)
    ]
