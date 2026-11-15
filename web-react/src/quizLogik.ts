// Reine Logik ohne React: leicht testbar (siehe quizLogik.test.ts)
import type { Buchstabe, JokerTyp } from "./api/types";

export const ANZAHL_FRAGEN = 15;
export const SEKUNDEN_PRO_FRAGE = 30;
export const ALLE_JOKER: JokerTyp[] = ["5050", "telefon", "publikum", "skip", "doppel"];
export const JOKER_SYMBOL: Record<JokerTyp, string> = {
  "5050": "50:50", telefon: "📞", publikum: "👥", skip: "⏭", doppel: "✌️",
};

/** Fortschritt in Prozent für den Balken oben. */
export function fortschritt(level: number, total = ANZAHL_FRAGEN): number {
  return Math.round(((level - 1) / total) * 100);
}

/** Name prüfen, bevor er an den Server geht (Server prüft zusätzlich). */
export function nameGueltig(name: string): boolean {
  const n = name.trim();
  return n.length >= 1 && n.length <= 20 && !/[<>]/.test(n);
}

/** Ist das Spiel nach dieser Antwort vorbei? */
export function spielVorbei(richtig: boolean, level: number, total = ANZAHL_FRAGEN): boolean {
  return !richtig || level >= total;
}

/** Antworten, die (noch) angeklickt werden dürfen. */
export function waehlbar(alle: Buchstabe[], entfernt: Buchstabe[], gesperrt: Buchstabe[]): Buchstabe[] {
  return alle.filter((b) => !entfernt.includes(b) && !gesperrt.includes(b));
}
