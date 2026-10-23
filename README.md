<div align="center">

# 🧠 IQ Quiz

**Ein Quiz im Stil der großen TV-Quizshows — Full-Stack-App mit 515 Fragen, 7 Sprachen, Preisleiter & Jokern.**
*(Unterhaltung, kein wissenschaftlicher IQ-Test.)*

[![Live](https://img.shields.io/badge/Live-Spielen-2563eb?style=for-the-badge&logo=github)](https://enesdoudouzi-sys.github.io/iq-quiz-v2)
&nbsp;
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-Android-5A0FC8?style=for-the-badge&logo=pwa&logoColor=white)

### 👉 [**Jetzt spielen**](https://enesdoudouzi-sys.github.io/iq-quiz-v2)

</div>

---

## 📖 Über das Projekt

Eine komplette **Full-Stack-Quiz-App**: Python/FastAPI-Backend mit Datenbank & Auth, dazu ein Frontend als **PWA** und eine **Android-App** (Capacitor). Von der Datenbank bis zur App im Store — alles selbst gebaut.

**Was dieses Projekt zeigt:** REST-API-Design · Datenbank (SQLite/SQLAlchemy) · JWT-Auth · Rate-Limiting · Mehrsprachigkeit · PWA & Mobile-Packaging · Deployment (Render + GitHub Pages).

## 🎮 Features

| Feature | Beschreibung |
|---|---|
| ✅ 515 Fragen | Zufällig aus 17 Kategorien |
| ⏱️ Timer | 20 / 25 / 30 Sek pro Level |
| 🧠 Live IQ | Aktualisiert nach jeder Frage |
| 💰 Preisleiter | WWM-Style mit Sicherheitsstufen |
| ☠️ Game Over | Falsche Antwort = ausgeschieden |
| 🃏 3 Joker | 50:50 · Telefon · Publikum |
| 🌍 7 Sprachen | DE · EN · TR · FR · ES · PT · AR |
| 🏆 Highscores | Top 10 in SQLite-Datenbank |
| 🔊 Sounds | Richtig / Falsch / Gewonnen |
| 📱 Mobile | Responsive + PWA + Android (Capacitor) |

## 🛠️ Tech-Stack

| Backend | Frontend | Hosting |
|---|---|---|
| Python 3.13 · FastAPI | HTML5 · CSS3 · JavaScript | Render.com (API) |
| SQLite · SQLAlchemy | PWA / Service Worker | GitHub Pages (Frontend) |
| JWT-Auth · Rate-Limiting | Capacitor (Android/iOS) | |

## 🔒 Sicherheit

| Maßnahme | Umsetzung |
|---|---|
| ✅ CORS | Nur erlaubte Herkünfte |
| ✅ Rate-Limiting | 10 Starts / 60 Antworten pro Minute |
| ✅ Input-Validierung | Alle Eingaben geprüft |
| ✅ HTTPS | Automatisch via Render |
| ✅ Session-Limit | Max. 1000 gleichzeitig |

## 🚀 Lokal starten

```bash
git clone https://github.com/enesdoudouzi-sys/iq-quiz-v2.git
cd iq-quiz-v2/backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn main:app --reload      # http://localhost:8000
```

**Android-App bauen:**
```bash
npx cap sync android
npx cap open android
```

---

<div align="center">

Entwickelt von **Enes Doudouzi** · [@enesdoudouzi-sys](https://github.com/enesdoudouzi-sys)

</div>
