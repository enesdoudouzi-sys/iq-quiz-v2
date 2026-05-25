# 🧠 IQ Quiz Web App

Ein vollständiges Full-Stack IQ-Test Projekt im "Wer wird Millionär" Format.

## 🎮 Features

- 15 Fragen pro Runde aus einem Pool von 105 Fragen
- 3 Kategorien: Allgemeinwissen, Logik & Zahlenfolgen, Konzentration
- Timer pro Frage (20/25/30 Sekunden)
- Live IQ-Anzeige nach jeder Frage
- Preisleiter wie bei Wer wird Millionär
- Falsche Antwort = sofort ausgeschieden
- 3 Joker: 50:50 / Telefon / Publikum
- Highscore System
- Sound Effekte
- Animationen

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, SQLite, JWT Auth
- **Frontend:** HTML5, CSS3, JavaScript
- **Hosting:** GitHub Pages + Render.com

## 🚀 Installation

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn main:app --reload
```

Browser öffnen: http://localhost:8000

## 📁 Struktur
