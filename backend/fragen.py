import random
import re
import os
import json
import hashlib

# schwierigkeit: 1=leicht, 2=mittel, 3=schwer
# erklaerung: kurze Erklaerung warum die Antwort richtig ist

# Alle Fragen liegen in daten/fragen.json (nicht mehr im Python-Code).
# Neue Fragen: dort einen Eintrag hinzufügen – Format:
#   {"kategorie": "...", "schwierigkeit": 1-3, "frage": "...",
#    "antworten": {"A": "...", "B": "...", "C": "...", "D": "..."},
#    "richtig": "A"-"D", "erklaerung": "...", "seq": null}
# Danach die Tests laufen lassen (prüfen Format und Duplikate).
_FRAGEN_DATEI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "daten", "fragen.json")
with open(_FRAGEN_DATEI, encoding="utf-8") as _f:
    ALLE_FRAGEN = json.load(_f)

SICHERHEITSSTUFEN = [5, 10, 15]

IQ_TABELLE = {}
for i in range(0, 51):
    if i == 0:
        IQ_TABELLE[i] = 85
    elif i <= 5:
        IQ_TABELLE[i] = 85 + i * 3
    elif i <= 10:
        IQ_TABELLE[i] = 100 + (i-5) * 3
    elif i <= 15:
        IQ_TABELLE[i] = 115 + (i-10) * 3
    elif i <= 20:
        IQ_TABELLE[i] = 130 + (i-15) * 3
    else:
        IQ_TABELLE[i] = min(145, 145 + (i-20))

PREISE_LISTE = ['100 EUR','200 EUR','300 EUR','500 EUR','1.000 EUR','2.000 EUR','4.000 EUR','8.000 EUR','16.000 EUR','32.000 EUR','64.000 EUR','125.000 EUR','250.000 EUR','500.000 EUR','1.000.000 EUR']

PREISSTUFEN = {}
for i in range(1, 51):
    PREISSTUFEN[i] = PREISE_LISTE[min(i-1, len(PREISE_LISTE)-1)]

IQ_BEZEICHNUNG = {
    range(0,   86): "Unterdurchschnittlich",
    range(86,  95): "Leicht unterdurchschnittlich",
    range(95, 105): "Durchschnittlich",
    range(105,115): "Überdurchschnittlich",
    range(115,125): "Intelligent",
    range(125,135): "Hochbegabt",
    range(135,200): "Ausnahmetalent",
}

# ── Übersetzungen der Fragen ────────────────────────────────────────────────
# Dateien uebersetzungen/<sprache>.json: { frage_id: {"frage": ..., "antworten": [A, B, C, D], "erklaerung": ...} }
# Die Antworten stehen in der Original-Reihenfolge A–D (vor dem Mischen).
# Fehlt eine Übersetzung, bleibt die deutsche Frage.
def frage_id(frage):
    return hashlib.sha1(frage["frage"].strip().encode("utf-8")).hexdigest()[:10]

_UEBERSETZUNGEN = {}
_UE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uebersetzungen")
if os.path.isdir(_UE_DIR):
    for _datei in os.listdir(_UE_DIR):
        if _datei.endswith(".json"):
            with open(os.path.join(_UE_DIR, _datei), encoding="utf-8") as _f:
                _UEBERSETZUNGEN[_datei[:-5]] = json.load(_f)

SPRACHEN = ["de"] + sorted(_UEBERSETZUNGEN)

def _uebersetze(frage, sprache):
    u = _UEBERSETZUNGEN.get(sprache, {}).get(frage_id(frage))
    if not u or len(u.get("antworten", [])) != 4:
        return frage
    frage["frage"] = u["frage"]
    frage["antworten"] = dict(zip(["A", "B", "C", "D"], u["antworten"]))
    if u.get("erklaerung"):
        frage["erklaerung"] = u["erklaerung"]
    frage["sprache"] = sprache
    return frage

def _mische_antworten(frage, rng):
    """Antworten in zufällige Reihenfolge bringen und 'richtig' anpassen.
    Ohne das wäre die richtige Antwort in 41 % der Fragen 'C'."""
    keys = ["A", "B", "C", "D"]
    texte = [frage["antworten"][k] for k in keys]
    richtig_text = frage["antworten"][frage["richtig"]]
    rng.shuffle(texte)
    frage["antworten"] = dict(zip(keys, texte))
    frage["richtig"] = keys[texte.index(richtig_text)]
    return frage

def _ansteigende_auswahl(pool, anzahl, rng):
    """Wie bei TV-Quizshows: Fragen 1-5 leicht, 6-10 mittel, 11-15 schwer.
    Fehlen Fragen einer Stufe (z. B. kleine Kategorie), wird mit der
    nächstliegenden Stufe aufgefüllt."""
    stufen = {1: [], 2: [], 3: []}
    for f in pool:
        stufen.get(f.get("schwierigkeit", 2), stufen[2]).append(f)
    for liste in stufen.values():
        rng.shuffle(liste)
    plan = [1] * 5 + [2] * 5 + [3] * 5
    plan = (plan + [3] * anzahl)[:anzahl] if anzahl > 15 else plan[:anzahl]
    ersatz = {1: [1, 2, 3], 2: [2, 1, 3], 3: [3, 2, 1]}
    auswahl = []
    for soll in plan:
        for s in ersatz[soll]:
            if stufen[s]:
                auswahl.append(stufen[s].pop())
                break
    return auswahl

def _baue_runde(pool, anzahl, rng, sprache="de"):
    fragen = []
    for i, f in enumerate(_ansteigende_auswahl(pool, anzahl, rng)):
        frage = dict(f)
        frage["antworten"] = dict(f["antworten"])
        _uebersetze(frage, sprache)
        _mische_antworten(frage, rng)
        frage["level"] = i + 1
        fragen.append(frage)
    return fragen

def get_daily_fragen(date_str, anzahl=15, sprache="de"):
    # Gleicher Seed pro Tag: alle Spieler bekommen dieselben Fragen in derselben Reihenfolge
    rng = random.Random(date_str)
    return _baue_runde(ALLE_FRAGEN, anzahl, rng, sprache)

def get_random_fragen(anzahl=15, kategorie='alle', schwierigkeit='alle', sprache='de'):
    rng = random.Random()
    if kategorie == 'alle':
        pool = ALLE_FRAGEN
    else:
        pool = [f for f in ALLE_FRAGEN if f['kategorie'] == kategorie]
        if len(pool) < anzahl:
            pool = ALLE_FRAGEN

    if schwierigkeit != 'alle':
        # Feste Schwierigkeit gewählt: keine ansteigende Reihenfolge
        try:
            sv = int(schwierigkeit)
            filtered = [f for f in pool if f.get('schwierigkeit', 2) == sv]
            if len(filtered) >= anzahl:
                pool = list(filtered)
                rng.shuffle(pool)
                fragen = []
                for i, f in enumerate(pool[:anzahl]):
                    frage = dict(f)
                    frage["antworten"] = dict(f["antworten"])
                    _uebersetze(frage, sprache)
                    _mische_antworten(frage, rng)
                    frage["level"] = i + 1
                    fragen.append(frage)
                return fragen
        except ValueError:
            pass

    return _baue_runde(pool, anzahl, rng, sprache)
