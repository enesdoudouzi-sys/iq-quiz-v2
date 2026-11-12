"""Automatische Tests für den Quiz-Server.

Ausführen (im Ordner backend):  python -m pytest -q
"""
import collections
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("ADMIN_TOKEN", "test-token")


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # eigene SQLite-Datei pro Test
    for mod in ("main", "database"):
        sys.modules.pop(mod, None)
    from fastapi.testclient import TestClient
    import main
    main.limiter.enabled = False
    return TestClient(main.app), main


def richtig(main, sid, level):
    return next(f for f in main.sessions[sid]["fragen"] if f["level"] == level)["richtig"]


def falsch(main, sid, level):
    return next(k for k in "ABCD" if k != richtig(main, sid, level))


def neues_spiel(c, name="Tester"):
    return c.post("/api/start", json={"name": name}).json()["session_id"]


# ── Fragen ────────────────────────────────────────────────────────────────
def test_fragen_ohne_duplikate_und_vollstaendig():
    import fragen as F
    texte = [f["frage"].strip().lower() for f in F.ALLE_FRAGEN]
    assert len(texte) == len(set(texte))
    for f in F.ALLE_FRAGEN:
        assert set(f["antworten"]) == {"A", "B", "C", "D"}
        assert f["richtig"] in "ABCD"
        assert len(set(f["antworten"].values())) == 4
        assert f.get("erklaerung")
        assert f["schwierigkeit"] in (1, 2, 3)


def test_antworten_gleichmaessig_verteilt():
    import fragen as F
    zaehler = collections.Counter()
    for _ in range(300):
        zaehler.update(f["richtig"] for f in F.get_random_fragen(15))
    gesamt = sum(zaehler.values())
    for k in "ABCD":
        assert 0.20 < zaehler[k] / gesamt < 0.30


def test_schwierigkeit_steigt():
    import fragen as F
    stufen = [f["schwierigkeit"] for f in F.get_random_fragen(15)]
    assert stufen == [1] * 5 + [2] * 5 + [3] * 5


def test_tages_challenge_fuer_alle_gleich():
    import fragen as F
    a, b = F.get_daily_fragen("2026-01-01"), F.get_daily_fragen("2026-01-01")
    assert [(f["frage"], f["richtig"]) for f in a] == [(f["frage"], f["richtig"]) for f in b]


# ── Spielablauf ───────────────────────────────────────────────────────────
def test_frage_verraet_keine_loesung(client):
    c, _ = client
    sid = neues_spiel(c)
    assert "richtig" not in c.get(f"/api/frage/{sid}/1").json()


def test_level_reihenfolge_wird_erzwungen(client):
    c, main = client
    sid = neues_spiel(c)
    r = c.post("/api/antwort", json={"session_id": sid, "level": 2, "antwort": "A"})
    assert r.status_code == 400


def test_doppel_chance_und_ueberspringen(client):
    c, main = client
    sid = neues_spiel(c)
    assert c.post("/api/joker", json={"session_id": sid, "level": 1, "typ": "doppel"}).status_code == 200
    r = c.post("/api/antwort", json={"session_id": sid, "level": 1, "antwort": falsch(main, sid, 1)}).json()
    assert r == {"richtig": False, "zweiter_versuch": True}
    assert c.post("/api/antwort", json={"session_id": sid, "level": 1, "antwort": richtig(main, sid, 1)}).json()["richtig"]
    assert c.post("/api/joker", json={"session_id": sid, "level": 2, "typ": "skip"}).json() == {"typ": "skip"}
    assert c.post("/api/antwort", json={"session_id": sid, "level": 3, "antwort": richtig(main, sid, 3)}).json()["richtig"]
    assert c.post("/api/joker", json={"session_id": sid, "level": 4, "typ": "skip"}).status_code == 400


# ── Bestenliste ───────────────────────────────────────────────────────────
def test_highscore_nur_mit_echtem_spiel(client):
    c, _ = client
    r = c.post("/api/highscores", json={"name": "Hacker", "iq": 200, "level": 15})
    assert r.status_code == 400


def test_highscore_wert_kommt_vom_server(client):
    c, main = client
    sid = neues_spiel(c)
    for lvl in range(1, 4):
        c.post("/api/antwort", json={"session_id": sid, "level": lvl, "antwort": richtig(main, sid, lvl)})
    c.post("/api/antwort", json={"session_id": sid, "level": 4, "antwort": falsch(main, sid, 4)})
    for lvl in range(5, 16):  # Weiterspielen erhöht das Ergebnis nicht mehr
        c.post("/api/antwort", json={"session_id": sid, "level": lvl, "antwort": richtig(main, sid, lvl)})
    assert c.post("/api/highscores", json={"name": "Enes", "iq": 200, "level": 15, "session_id": sid}).json() == {"ok": True}
    eintrag = c.get("/api/highscores").json()[0]
    assert eintrag["iq"] < 200 and eintrag["level"] == 3
    # nur einmal pro Spiel
    assert c.post("/api/highscores", json={"name": "Enes", "iq": 1, "level": 1, "session_id": sid}).status_code == 400


@pytest.mark.parametrize("name", ["F1ck dich", "   "])
def test_ungueltige_namen_werden_abgelehnt(client, name):
    c, _ = client
    assert c.post("/api/start", json={"name": name}).status_code == 422


def test_html_im_namen_wird_entfernt(client):
    c, main = client
    sid = neues_spiel(c, "<b>Enes</b>")
    assert "<" not in main.sessions[sid]["name"] and ">" not in main.sessions[sid]["name"]


def test_wochen_bestenliste(client):
    c, main = client
    import database
    from datetime import datetime, timedelta
    for name in ("Alt", "Neu"):
        sid = neues_spiel(c, name)
        c.post("/api/antwort", json={"session_id": sid, "level": 1, "antwort": richtig(main, sid, 1)})
        c.post("/api/highscores", json={"name": name, "iq": 0, "level": 0, "session_id": sid})
    db = database.SessionLocal()
    db.query(database.Highscore).filter_by(name="Alt").update({"datum": datetime.now() - timedelta(days=10)})
    db.commit()
    assert {e["name"] for e in c.get("/api/highscores").json()} == {"Alt", "Neu"}
    assert [e["name"] for e in c.get("/api/highscores?zeitraum=woche").json()] == ["Neu"]


# ── Betreiber-Endpunkte ───────────────────────────────────────────────────
def test_statistik_und_kontakt_nur_mit_token(client):
    c, _ = client
    assert c.post("/api/log", json={"typ": "fehler", "info": "Test"}).json() == {"ok": True}
    assert c.post("/api/log", json={"typ": "unbekannt"}).status_code == 422
    assert c.get("/api/statistik").status_code == 403
    stat = c.get("/api/statistik", headers={"X-Admin-Token": "test-token"}).json()
    assert stat["fehler"] == 1
    assert c.post("/api/kontakt", json={"name": "A", "email": "a@b.de", "nachricht": "Hallo Welt"}).json() == {"ok": True}
    assert c.get("/api/kontakt").status_code == 403
    assert len(c.get("/api/kontakt", headers={"X-Admin-Token": "test-token"}).json()) == 1
