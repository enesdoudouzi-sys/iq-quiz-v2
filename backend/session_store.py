"""Speicher für laufende Spiele (Sessions).

Funktioniert wie ein normales dict (sessions[sid], sid in sessions, ...),
damit main.py kaum geändert werden muss. Zusätzlich:

* Ein Zwischenspeicher im Arbeitsspeicher macht Lesezugriffe schnell.
* Fehlt eine Session im Speicher (z. B. nach Neustart), wird sie aus der
  Datenbank geladen.
* Nach jeder API-Anfrage schreibt flush() alle Sessions, die in dieser
  Anfrage benutzt wurden, in die Datenbank.
"""
import json
import threading
from datetime import datetime, timedelta

from database import SessionLocal, SpielSession


class SessionStore:
    def __init__(self, ttl_sekunden: int):
        self._cache: dict[str, dict] = {}
        self._benutzt: set[str] = set()
        self._lock = threading.Lock()
        self.ttl = ttl_sekunden

    # ---- dict-ähnliche Schnittstelle ----
    def get(self, sid, default=None):
        if not sid:
            return default
        with self._lock:
            daten = self._cache.get(sid)
        if daten is None:
            daten = self._laden(sid)
        if daten is None:
            return default
        with self._lock:
            self._cache[sid] = daten
            self._benutzt.add(sid)
        return daten

    def __getitem__(self, sid):
        daten = self.get(sid)
        if daten is None:
            raise KeyError(sid)
        return daten

    def __contains__(self, sid):
        return self.get(sid) is not None

    def __setitem__(self, sid, daten):
        with self._lock:
            self._cache[sid] = daten
            self._benutzt.add(sid)

    def __delitem__(self, sid):
        with self._lock:
            self._cache.pop(sid, None)
            self._benutzt.discard(sid)
        with SessionLocal() as db:
            db.query(SpielSession).filter(SpielSession.id == sid).delete()
            db.commit()

    def __len__(self):
        with self._lock:
            return len(self._cache)

    # ---- Datenbank ----
    def _laden(self, sid):
        with SessionLocal() as db:
            row = db.get(SpielSession, sid)
            if row is None:
                return None
            if row.aktualisiert < datetime.now() - timedelta(seconds=self.ttl):
                return None  # abgelaufen
            return json.loads(row.daten)

    def flush(self):
        """Benutzte Sessions in die Datenbank schreiben (nach jeder Anfrage)."""
        with self._lock:
            ids = list(self._benutzt)
            self._benutzt.clear()
            zu_speichern = {sid: self._cache[sid] for sid in ids if sid in self._cache}
        if not zu_speichern:
            return
        with SessionLocal() as db:
            for sid, daten in zu_speichern.items():
                db.merge(SpielSession(id=sid, daten=json.dumps(daten), aktualisiert=datetime.now()))
            db.commit()

    def aufraeumen(self, max_im_speicher: int = 1000):
        """Abgelaufene Sessions löschen und den Zwischenspeicher begrenzen."""
        grenze = datetime.now() - timedelta(seconds=self.ttl)
        with SessionLocal() as db:
            db.query(SpielSession).filter(SpielSession.aktualisiert < grenze).delete()
            db.commit()
        with self._lock:
            if len(self._cache) > max_im_speicher:
                # älteste aus dem Speicher werfen; sie bleiben in der Datenbank
                for sid in list(self._cache)[: len(self._cache) - max_im_speicher]:
                    if sid not in self._benutzt:
                        del self._cache[sid]
