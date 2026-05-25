# 🧠 IQ Quiz – Wer wird Millionär Format

> Ein vollständiges Full-Stack Web-Projekt von **Enes Doudouzi**

🌐 **Live:** https://enesdoudouzi-sys.github.io/iq-quiz-v2  
⚙️ **API:** https://iq-quiz-v2.onrender.com

---

## 🎮 Features

| Feature | Beschreibung |
|---|---|
| 🎯 105 Fragen | Zufällig gemischt aus 3 Kategorien |
| ⏱️ Timer | 20 / 25 / 30 Sekunden pro Frage |
| 🧠 Live IQ | Wird nach jeder Frage aktualisiert |
| 💰 Preisleiter | Wie bei Wer wird Millionär |
| ☠️ Game Over | Falsche Antwort = sofort ausgeschieden |
| 🃏 3 Joker | 50:50 · Telefon · Publikum |
| 🏆 Highscores | Top 10 gespeichert in Datenbank |
| 🔊 Sounds | Effekte bei richtig / falsch / Gewonnen |
| ✨ Animationen | Smooth Übergänge und Feedback |

---

## 🛠️ Tech Stack

### Backend
- **Python 3.13** – Programmiersprache
- **FastAPI** – REST API Framework
- **SQLite + SQLAlchemy** – Datenbank
- **JWT Authentication** – Login System
- **Rate Limiting** – Sicherheit gegen Spam
- **CORS** – Nur erlaubte Domains

### Frontend
- **HTML5** – Struktur
- **CSS3** – Design (Dark Mode, Animationen)
- **JavaScript** – Spiellogik, API-Calls

### Deployment
- **Render.com** – Backend Hosting (Free Tier)
- **GitHub Pages** – Frontend Hosting

---

## 🚀 Lokal starten

```bash
# Repository klonen
git clone https://github.com/enesdoudouzi-sys/iq-quiz-v2.git
cd iq-quiz-v2/backend

# Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Pakete installieren
pip install -r requirements.txt

# Server starten
python3 -m uvicorn main:app --reload
```

Browser öffnen: **http://localhost:8000**

---



## 👨‍💻 Entwickler

**Enes Doudouzi**  
GitHub: [@enesdoudouzi-sys](https://github.com/enesdoudouzi-sys)

---

*Entwickelt mit Python, FastAPI und JavaScript*
