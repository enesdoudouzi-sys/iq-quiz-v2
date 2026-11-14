<div align="center">

# 🧠 IQ Quiz

**Full-Stack-Quiz-App mit 551 Fragen in 17 Kategorien, 3 Sprachen, 6 Jokern, Bestenliste und Tagesquiz.**
*(Unterhaltung, kein wissenschaftlicher IQ-Test.)*

[![Live](https://img.shields.io/badge/Live-Spielen-2563eb?style=for-the-badge&logo=github)](https://enesdoudouzi-sys.github.io/iq-quiz-v2)
&nbsp;
![Python](https://img.shields.io/badge/Python-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Android](https://img.shields.io/badge/Android-Capacitor-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![React](https://img.shields.io/badge/React-TypeScript-3178C6?style=for-the-badge&logo=react&logoColor=white)

### 👉 [**Jetzt spielen**](https://enesdoudouzi-sys.github.io/iq-quiz-v2) · [**Android-App**](https://enesdoudouzi-sys.github.io/iq-quiz-v2/download.html)

</div>

![IQ Quiz Vorschau](screenshots/start.png)

---

## 📖 Was die App macht

- **551 Fragen** in 17 Kategorien, auf **Deutsch, Englisch und Türkisch**
- Pro Runde **15 Fragen**, die immer schwerer werden, mit Timer
- **6 Joker**, z. B. 50:50, Telefon, Publikum, Überspringen und Doppelte Chance
- **IQ-Auswertung** am Ende
- **Bestenliste:** gesamt und wöchentlich
- **Tagesquiz:** Alle Spieler bekommen am selben Tag dieselben Fragen.
- **Plattformen:** Website, Android-App (Google Play) und itch.io

## 🏗️ Architektur

```
Handy-App / Website / itch.io   →   Server (REST-API)   →   Datenbank
 HTML, CSS, JavaScript             Python + FastAPI         PostgreSQL
 Capacitor (Android)               gehostet auf Render      (SQLite lokal)
```

### Der Weg einer Antwort (der wichtigste Ablauf)
1. Der Spieler tippt auf „B“. `app.js` schickt eine **HTTP-POST-Anfrage** an `/api/antwort`.
2. Der Server (`backend/main.py`) prüft, ob die Antwort richtig ist, und schickt **JSON** zurück, z. B. `{"richtig": true, "iq": 110}`.
3. `app.js` liest das JSON und färbt den Knopf grün oder rot.

## 📁 Projektstruktur

```
iq-quiz-v2/
├── index.html, style.css      → Website: Inhalt (HTML) und Design (CSS)
├── app.js                     → Website: Logik (JavaScript, Spielablauf)
├── i18n.js                    → Oberflächentexte in DE / EN / TR
├── datenschutz.html …         → Rechtliche Seiten
├── www/                       → Kopie der Website für die Android-App
├── android/                   → Android-Projekt (Capacitor), daraus entsteht das AAB
├── backend/                   → Server (Python)
│   ├── main.py                → API-Endpunkte (/api/start, /api/antwort, /api/joker …)
│   ├── fragen.py              → Fragen, Mischen, Schwierigkeit, Übersetzung
│   ├── fragen_extra.py        → Weitere Fragen-Kategorien
│   ├── database.py            → Datenbank-Tabellen (SQLAlchemy)
│   ├── uebersetzungen/        → en.json, tr.json
│   └── tests/                 → Automatische Tests (pytest)
└── web-react/                 → Neues Frontend in React + TypeScript + Tailwind + Vite (in Arbeit)
```

## 🛠️ Tech-Stack

| Bereich | Technik |
|---|---|
| Frontend | HTML5 · CSS3 · JavaScript · Service Worker (offline) |
| Frontend (neu) | React · TypeScript · Tailwind CSS · Vite · Vitest |
| Mobile | Capacitor (Android-App, AAB für Google Play) |
| Backend | Python · FastAPI · Pydantic · slowapi |
| Datenbank | PostgreSQL (Produktion) · SQLite (lokal) · SQLAlchemy |
| Hosting | Render (API) · GitHub Pages (Website) · itch.io |
| Qualität | pytest (18 Tests) · Git-Branches und Pull Requests |
| KI | Entwickelt mit Claude Code (Agentic Coding) |

## 💡 Wichtige technische Entscheidungen

**Die richtige Antwort bleibt auf dem Server**
Alles im Browser kann der Nutzer lesen. Deshalb schickt der Server nur Frage und Antwortmöglichkeiten. Ob eine Antwort richtig ist und welcher IQ herauskommt, berechnet nur der Server.

**Highscores sind fälschungssicher**
Jedes Spiel bekommt eine Session-ID. Ein Highscore lässt sich nur mit einer gültigen Session eintragen, und nur einmal pro Spiel. Der IQ kommt dabei aus der Session, nicht vom Client. Nach der ersten falschen Antwort wird das Ergebnis eingefroren.

**Rate-Limit**
`slowapi` zählt die Anfragen pro IP-Adresse, z. B. höchstens 10 Spielstarts pro Minute. Bei mehr kommt der Fehler 429. Die IP kommt aus dem letzten Eintrag von `X-Forwarded-For`, den Render setzt, und lässt sich deshalb nicht fälschen. Hinter Cloudflare gilt `CF-Connecting-IP`, aber nur bei Anfragen, die nachweislich von Cloudflare kommen.

**Faire Fragen**
Die Antworten werden zufällig gemischt, die Schwierigkeit steigt im Lauf der Runde. Das Tagesquiz nutzt einen Seed aus dem Datum: Alle bekommen dieselben Fragen, ohne dass etwas gespeichert werden muss.

**Übersetzungen**
Jede Frage hat eine feste ID, einen SHA-1-Hash des Fragetexts. Die Übersetzung wird über diese ID eingesetzt, bevor die Antworten gemischt werden. So bleibt die richtige Antwort in jeder Sprache korrekt.

## 🔒 Sicherheit

| Maßnahme | Umsetzung |
|---|---|
| SQL-Injection | SQLAlchemy übergibt Werte als Parameter, nie als zusammengebauten SQL-Text |
| Eingaben | Pydantic-Validatoren prüfen Länge und Zeichen; Namensfilter gegen Beleidigungen |
| Admin-Endpunkte | `X-Admin-Token`, Vergleich mit `hmac.compare_digest` (Schutz vor Timing-Angriffen) |
| CORS | Nur die eigenen Domains dürfen die API aufrufen |
| Spam | Honeypot-Feld im Kontaktformular |
| Server-Speicher | Sessions laufen nach 3 Stunden ab, höchstens 1.000 gleichzeitig |
| Fehler-Statistik | Anonym; Einträge werden nach 90 Tagen gelöscht |

## 🚀 Lokal starten

**Backend:**
```bash
git clone https://github.com/enesdoudouzi-sys/iq-quiz-v2.git
cd iq-quiz-v2/backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python3 -m uvicorn main:app --reload      # http://localhost:8000
python3 -m pytest                         # Tests ausführen
```

**Neues React-Frontend:**
```bash
cd web-react
npm install
npm run dev        # Entwicklungsserver
npm test           # Tests ausführen
npm run build      # fertige Dateien in dist/
```

**Android-App bauen:**
```bash
npx cap sync android
cd android && ./gradlew bundleRelease
```

## 📚 Lernplan (Weg zum KI-Softwareentwickler)

| Woche | Thema | Woran gelernt wird | Aufgabe |
|---|---|---|---|
| 1 | JavaScript-Logik: Variablen, `if`, Schleifen, Funktionen, Arrays | `web-react/src/quizLogik.ts` | `SEKUNDEN_PRO_FRAGE` von 30 auf 20 ändern und die Tests laufen lassen |
| 2 | HTTP: GET/POST, JSON, Statuscodes 200/400/404/429 | `web-react/src/api/client.ts` | Browser-Entwicklertools (F12 → Netzwerk), eine Runde spielen, jede Anfrage ansehen |
| 3 | Git: `status`, `add`, `commit`, `push`, `branch`, Pull Requests | dieses Repository | Eine kleine Änderung komplett allein machen |
| 4+ | React, TypeScript, Supabase (Login), Docker, Node.js/Express, n8n | `web-react/` und neue Teile | Eins nach dem anderen |

**Regeln:**
- Ein Thema pro Sitzung.
- Ich mache den ersten Versuch selbst, die KI hilft und erklärt.
- Wichtige Dinge vor neuen Technologien.

## 🗺️ Roadmap

- [x] Website, Android-App, itch.io
- [x] 551 Fragen in 3 Sprachen, Tests, Sicherheit
- [ ] Google Play: geschlossener Test (12 Tester, 14 Tage), danach öffentlich
- [ ] Dauerhafte Datenbank (Neon/Postgres) aktivieren
- [ ] Neues Frontend in React + TypeScript live schalten
- [ ] Spieler-Login mit Supabase
- [ ] Docker, Cloudflare, GitHub Actions, n8n-Automatisierung

---

<div align="center">

Entwickelt von **Enes Doudouzi** · [@enesdoudouzi-sys](https://github.com/enesdoudouzi-sys)

</div>
