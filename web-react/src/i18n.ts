import type { Sprache } from "./api/types";

// Alle Texte der Oberfläche in drei Sprachen. Die Fragen selbst übersetzt der Server.
const TEXTE = {
  de: {
    titel: "IQ Quiz", name: "Dein Name", start: "Quiz starten", daily: "📅 Tagesquiz",
    bestenliste: "🏆 Bestenliste", laedt: "Lädt…", frage: "Frage", richtig: "✅ Richtig!",
    falsch: "❌ Leider falsch", zeitAus: "⏱ Zeit abgelaufen", weiter: "Weiter",
    nochmal: "Nochmal versuchen – Doppelte Chance!", ergebnis: "Dein Ergebnis",
    eintragen: "In Bestenliste eintragen", gespeichert: "✔ Gespeichert", neu: "Nochmal spielen",
    zurueck: "Zurück", alle: "Gesamt", woche: "Woche", heute: "Heute", leer: "Noch keine Einträge",
    telefon: "Dein Telefonjoker meint:", publikum: "Das Publikum stimmt ab:",
  },
  en: {
    titel: "IQ Quiz", name: "Your name", start: "Start quiz", daily: "📅 Daily quiz",
    bestenliste: "🏆 Leaderboard", laedt: "Loading…", frage: "Question", richtig: "✅ Correct!",
    falsch: "❌ Wrong", zeitAus: "⏱ Time's up", weiter: "Next",
    nochmal: "Try again – double chance!", ergebnis: "Your result",
    eintragen: "Add to leaderboard", gespeichert: "✔ Saved", neu: "Play again",
    zurueck: "Back", alle: "All time", woche: "Week", heute: "Today", leer: "No entries yet",
    telefon: "Your phone-a-friend says:", publikum: "The audience votes:",
  },
  tr: {
    titel: "IQ Quiz", name: "Adın", start: "Quiz'i başlat", daily: "📅 Günlük quiz",
    bestenliste: "🏆 Sıralama", laedt: "Yükleniyor…", frage: "Soru", richtig: "✅ Doğru!",
    falsch: "❌ Yanlış", zeitAus: "⏱ Süre doldu", weiter: "Devam",
    nochmal: "Tekrar dene – çift şans!", ergebnis: "Sonucun",
    eintragen: "Sıralamaya ekle", gespeichert: "✔ Kaydedildi", neu: "Tekrar oyna",
    zurueck: "Geri", alle: "Tüm zamanlar", woche: "Hafta", heute: "Bugün", leer: "Henüz kayıt yok",
    telefon: "Telefon jokerin diyor ki:", publikum: "Seyirci oyluyor:",
  },
} satisfies Record<Sprache, Record<string, string>>;

export type TextSchluessel = keyof typeof TEXTE.de;

export function texte(sprache: Sprache) {
  return (schluessel: TextSchluessel) => TEXTE[sprache][schluessel];
}

export function gespeicherteSprache(): Sprache {
  try {
    const s = localStorage.getItem("iq_lang");
    if (s === "de" || s === "en" || s === "tr") return s;
  } catch { /* privater Modus */ }
  const b = navigator.language.slice(0, 2);
  return b === "tr" ? "tr" : b === "de" ? "de" : "en";
}

export function spracheMerken(s: Sprache) {
  try { localStorage.setItem("iq_lang", s); } catch { /* egal */ }
}
