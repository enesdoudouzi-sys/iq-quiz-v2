"""Logging und Metriken (Observability).

* Strukturierte Logs: jede Zeile ist ein JSON-Objekt. Log-Systeme
  (Grafana Loki, Datadog, Render-Logs ...) können danach filtern.
  Aus Datenschutzgründen werden KEINE IP-Adressen und keine Session-IDs geloggt.
* Prometheus-Metriken unter /metrics: Anfragen, Antwortzeiten, Spiele, Antworten.
"""
import json
import logging
import sys
import time
from datetime import datetime, timezone

from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

# ---------- Logging ----------

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        eintrag = {
            "zeit": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "nachricht": record.getMessage(),
        }
        eintrag.update(getattr(record, "felder", {}))  # zusätzliche Felder aus extra={"felder": {...}}
        if record.exc_info:
            eintrag["fehler"] = self.formatException(record.exc_info)
        return json.dumps(eintrag, ensure_ascii=False)


def logging_einrichten(level: str = "INFO") -> logging.Logger:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level)
    # uvicorns eigenes Zugriffs-Log abschalten: wir loggen jede Anfrage selbst (ohne IP)
    logging.getLogger("uvicorn.access").disabled = True
    return logging.getLogger("iqquiz")


log = logging.getLogger("iqquiz")

# ---------- Metriken ----------

ANFRAGEN = Counter("iqquiz_http_requests_total", "HTTP-Anfragen", ["methode", "route", "status"])
DAUER = Histogram("iqquiz_http_request_dauer_sekunden", "Antwortzeit der HTTP-Anfragen", ["route"],
                  buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5))
SPIELE = Counter("iqquiz_spiele_gestartet_total", "Gestartete Spiele", ["modus", "sprache"])
ANTWORTEN = Counter("iqquiz_antworten_total", "Beantwortete Fragen", ["richtig"])
JOKER = Counter("iqquiz_joker_total", "Benutzte Joker", ["typ"])
SESSIONS_IM_SPEICHER = Gauge("iqquiz_sessions_im_speicher", "Laufende Spiele im Zwischenspeicher")


def route_von(request) -> str:
    """Routen-Vorlage statt echtem Pfad: /api/frage/{session_id}/{level}
    statt /api/frage/123.../4 – sonst entstehen unendlich viele Metrik-Reihen
    und Session-IDs landen in Logs."""
    route = request.scope.get("route")
    return getattr(route, "path", "nicht_gefunden")


def anfrage_erfassen(request, status: int, start: float) -> None:
    dauer = time.perf_counter() - start
    route = route_von(request)
    ANFRAGEN.labels(request.method, route, str(status)).inc()
    DAUER.labels(route).observe(dauer)
    log.info("anfrage", extra={"felder": {
        "methode": request.method, "route": route, "status": status, "dauer_ms": round(dauer * 1000, 1),
    }})


def metriken_text() -> tuple[bytes, str]:
    return generate_latest(), CONTENT_TYPE_LATEST
