# 🧠 IQ Quiz

> **Wer wird Millionär** – als IQ-Test. Entwickelt von Enes Doudouzi.

[![Live](https://img.shields.io/badge/Live-GitHub%20Pages-blue?style=flat-square)](https://enesdoudouzi-sys.github.io/iq-quiz-v2)
[![API](https://img.shields.io/badge/API-Render.com-green?style=flat-square)](https://iq-quiz-v2.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.13-yellow?style=flat-square)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-teal?style=flat-square)](https://fastapi.tiangolo.com)

---

## 🎮 Features

| Feature | Beschreibung |
|---|---|
| ✅ 105 Fragen | Zufällig aus 3 Kategorien |
| ⏱️ Timer | 20 / 25 / 30 Sek pro Level |
| 🧠 Live IQ | Aktualisiert nach jeder Frage |
| 💰 Preisleiter | WWM-Style mit Sicherheitsstufen |
| ☠️ Game Over | Falsche Antwort = ausgeschieden |
| 🃏 3 Joker | 50:50 · Telefon · Publikum |
| 🌍 6 Sprachen | DE · EN · TR · FR · ES · AR |
| 🏆 Highscores | Top 10 in SQLite Datenbank |
| 🔊 Sounds | Richtig / Falsch / Gewonnen |
| 📱 Mobile | Responsive + PWA ready |

---

## 🛠️ Tech Stack

| Backend | Frontend | Hosting |
|---|---|---|
| Python 3.13 | HTML5 | Render.com |
| FastAPI | CSS3 | GitHub Pages |
| SQLite | JavaScript | |
| SQLAlchemy | PWA / Service Worker | |
| JWT Auth | | |
| Rate Limiting | | |

---

## 🚀 Lokal starten

```bash
git clone https://github.com/enesdoudouzi-sys/iq-quiz-v2.git
cd iq-quiz-v2/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn main:app --reload
```

Browser: http://localhost:8000

---

## 📁 Struktur

iq-quiz-v2/
├── backend/
│   ├── main.py
│   ├── fragen.py
│   ├── database.py
│   ├── auth.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   └── app.js
└── www/

## 🔒 Sicherheit

| | |
|---|---|
| ✅ CORS | Nur GitHub Pages erlaubt |
| ✅ Rate Limiting | 10 Starts / 60 Antworten pro Minute |
| ✅ Input Check | Alle Eingaben validiert |
| ✅ HTTPS | Automatisch via Render.com |
| ✅ Session Limit | Max 1000 gleichzeitig |

---

## 📱 Mobile App

Gebaut mit **Capacitor** für Android & iOS.

```bash
npx cap sync android
npx cap open android
```

---

## 👨‍💻 Entwickler

**Enes Doudouzi**
GitHub: [@enesdoudouzi-sys](https://github.com/enesdoudouzi-sys)

---

*Entwickelt mit Python · FastAPI · JavaScript · Capacitor*
