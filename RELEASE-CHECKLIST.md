# Release-Checkliste Google Play (Version 1.2)

Alles hier braucht deine Konten oder Entscheidungen. Der Code ist dafür vorbereitet.

## 1. RevenueCat + Play-Produkte

**Play Console → Monetarisieren → Produkte → In-App-Produkte**
| Produkt-ID | Typ | Preis |
|---|---|---|
| `iq_premium_v1` | Nicht verbrauchbar (einmalig) | 2,99 € |
| `joker_pack_5` | Verbrauchbar | 1,99 € |

**RevenueCat-Dashboard** (app.revenuecat.com)
1. Projekt anlegen, Android-App mit Paketname `com.enesdoudouzi.iqtest` hinzufügen und das Google-Play-Dienstkonto verbinden.
2. Beide Produkte importieren.
3. Entitlement `premium` anlegen und mit `iq_premium_v1` verknüpfen.
4. Offering „current" mit zwei Packages anlegen: eines mit `iq_premium_v1`, eines mit `joker_pack_5`.
5. Unter *Project Settings → API Keys* den **Android Public SDK Key** (beginnt mit `goog_`) kopieren.
6. In `app.js` ganz oben `REVENUECAT_API_KEY_ANDROID = 'REPLACE_ME_ANDROID_KEY'` durch den Key ersetzen.
7. `www/` neu befüllen: `cp app.js www/app.js && npx cap sync android`.

## 2. Bauen und testen (Android Studio, JDK 21)

```
npm install
npx cap sync android
npx cap open android
```
Build → Generate Signed Bundle (AAB). Auf einem echten Gerät testen: Quiz, Kauf (Testkonto unter *Play Console → Lizenztests*), „Käufe wiederherstellen", Urkunde als PDF (nutzt `window.print()`, funktioniert in WebViews oft nicht).

## 3. Gewerbe und Impressum

- Verkauf in der App ist gewerblich: Gewerbe beim Gewerbeamt anmelden und Steuerfragen (Umsatzsteuer, Kleinunternehmerregelung § 19 UStG) mit Steuerberater klären.
- `impressum.html` (und `frontend/impressum.html`): zweite Kontaktmöglichkeit ergänzen (Telefonnummer oder Kontaktformular), ggf. USt-ID. Das TODO-Kommentar dort danach löschen.

## 4. Verträge zur Auftragsverarbeitung

- Render: Dashboard → Settings → Legal/Compliance, DPA akzeptieren. Log-Aufbewahrung nachsehen.
- RevenueCat: DPA unter revenuecat.com/dpa akzeptieren.
- Danach in `datenschutz.html` prüfen, ob „Speicherdauer" und „Verträge nach Art. 28" für dich stimmen, sonst anpassen.

## 5. Keystore (Passwort „iqtest2024" ist öffentlich)

Neuen Upload-Key erzeugen, Passwort im Passwort-Manager speichern:
```
keytool -genkeypair -v -keystore iqtest-upload.keystore -alias iqtest -keyalg RSA -keysize 2048 -validity 10000
```
`android/keystore.properties` (steht in `.gitignore`) nach Vorlage `keystore.properties.example` ausfüllen. Wenn die App schon bei Play liegt: *Play Console → Test und Veröffentlichung → App-Integrität → Upload-Schlüssel zurücksetzen* beantragen.

## 6. Play Console

- Neue private Entwicklerkonten: geschlossener Test mit mindestens 12 Testern über 14 Tage vor der Produktion (aktuelle Vorgabe in der Console prüfen).
- Data-Safety-Formular und Content-Rating-Fragebogen: Vorgaben stehen in `store-listing.txt`.
- Zielgruppe 13+, Kategorie Trivia.
- Datenschutz-URL: https://enesdoudouzi-sys.github.io/iq-quiz-v2/datenschutz.html
