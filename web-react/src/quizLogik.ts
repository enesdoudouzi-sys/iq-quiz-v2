// Reine Logik ohne React: leicht testbar (siehe quizLogik.test.ts)
export const ANZAHL_FRAGEN = 15;
export const SEKUNDEN_PRO_FRAGE = 30;

/** Fortschritt in Prozent für den Balken oben. */
export function fortschritt(level: number, total = ANZAHL_FRAGEN): number {
  return Math.round(((level - 1) / total) * 100);
}

/** Name prüfen, bevor er an den Server geht (Server prüft zusätzlich). */
export function nameGueltig(name: string): boolean {
  const n = name.trim();
  return n.length >= 1 && n.length <= 20 && !/[<>]/.test(n);
}
