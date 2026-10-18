# Sicherheit – was im Code erledigt ist und was du selbst tun musst

## Im Code umgesetzt
- **Fake-Highscores:** Bestenlisten-Einträge brauchen eine beendete Server-Session. IQ und Level werden vom Server berechnet, nicht vom Client. Einmal einreichbar, nur Modi Normal/Endless/Daily, pro Name und Tag nur bester Daily-Eintrag, Mindest-Antwortzeit 0,7 s.
- **Rate-Limit hinter Proxy:** Client-IP wird aus dem letzten vertrauenswürdigen `X-Forwarded-For`-Eintrag gelesen (`TRUSTED_PROXY_HOPS`, Standard 1 für Render). Header-Spoofing hilft nicht mehr. Diagnose: `/api/ip`.
- **Session-Flooding:** max. 30 Sessions pro IP (eigene älteste werden verdrängt), 5000 global, TTL 2 h, Body max. 10 KB.
- **Toter Code:** `auth.py`, User-Tabelle und ungenutzte Pakete (jose, passlib, bcrypt …) entfernt.
- **Pakete:** `requirements.txt` minimal; Dependabot aktiv (`.github/dependabot.yml`).
- **Android:** `allowBackup=false`.
- **CSP** im `index.html` (Verbindungen nur zu eigenem Backend und RevenueCat), Security-Header im Backend, Swagger/OpenAPI aus, CORS auf feste Origins inkl. `https://localhost` (Android-App).
- Namen werden von Steuer-/HTML-Zeichen bereinigt.

## Das musst du selbst tun
1. **Render → Environment:** `TRUSTED_PROXY_HOPS=1` (Standard). Optional `ALLOWED_ORIGINS`. Nach dem Merge neu deployen. Danach `https://iq-quiz-v2.onrender.com/api/ip` aufrufen: es muss deine echte IP zeigen.
2. **Keystore:** Passwort „iqtest2024“ steht in der Git-Historie → neuen Upload-Key erzeugen (Befehl in `RELEASE-CHECKLIST.md`), in der Play Console Upload-Schlüssel zurücksetzen, altes Keystore nicht mehr verwenden. Historie nicht umschreiben nötig.
3. **JWT_SECRET_KEY** in Render löschen (wird nicht mehr genutzt).
4. **GitHub:** Settings → Password and authentication → 2FA aktivieren; Settings → Branches → Regel für `main` (PR + Force-Push verbieten); Settings → Code security → Dependabot alerts, Secret scanning, Push protection an.
5. **Render:** Logs-Aufbewahrung prüfen (enthalten IPs), DPA akzeptieren.
6. **DDoS:** Eine eigene Domain bei Cloudflare (kostenloser Plan, Proxy an) vor Render schalten; dann `TRUSTED_PROXY_HOPS=2`, `ALLOWED_ORIGINS` anpassen und die API-URL in `app.js` ändern.
7. **Hinweis:** Render-SQLite ist flüchtig; Bestenlisten gehen bei Neustart verloren (für Dauerbetrieb Postgres nutzen).
