// Erzeugt den Ordner www/ (Inhalt der Android-App) aus den Website-Dateien.
// Aufruf: npm run build:www   (läuft auch automatisch vor "npm run cap:sync")
//
// Unterschiede zur Website:
//  - Blöcke zwischen <!-- nur-web --> und <!-- /nur-web --> in index.html
//    werden entfernt (PWA-Manifest, Service Worker, Link "App installieren").
//  - manifest.json, service-worker.js und download.html werden nicht kopiert.
//  - www/assets/ wird hier NICHT angefasst: Die App-Bilder (Icons, Splash)
//    werden dort separat gepflegt; die Website-Bilder in assets/ enthalten
//    zusätzlich Store-Grafiken, die nicht in die App gehören.
import { cpSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";

const ZIEL = "www";
const DATEIEN = ["app.js", "i18n.js", "style.css", "datenschutz.html", "impressum.html", "favicon.ico"];
const ALT = ["service-worker.js", "manifest.json"]; // gehören nicht in die App

mkdirSync(ZIEL, { recursive: true });
for (const f of DATEIEN) cpSync(f, `${ZIEL}/${f}`);
for (const f of ALT) if (existsSync(`${ZIEL}/${f}`)) rmSync(`${ZIEL}/${f}`);

const html = readFileSync("index.html", "utf8")
  .replace(/<!-- nur-web -->\n[\s\S]*?\n<!-- \/nur-web -->\n/g, "");
if (html.includes("nur-web")) {
  console.error("Fehler: Ein <!-- nur-web --> Block wurde nicht vollständig entfernt.");
  process.exit(1);
}
writeFileSync(`${ZIEL}/index.html`, html);

console.log(`www/ erzeugt: index.html + ${DATEIEN.length} Dateien`);
