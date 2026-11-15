# ---- IQ-Quiz Backend (FastAPI) ----
# Schlankes offizielles Python-Image
FROM python:3.12-slim

# Keine .pyc-Dateien, Logs sofort ausgeben
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Erst nur die Abhängigkeiten kopieren: Docker cached diesen Schritt,
# solange sich requirements.txt nicht ändert (schnellere Builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Dann den Code
COPY . .

# Nicht als root laufen (Sicherheit)
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Docker prüft selbst, ob der Server antwortet
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
