// Typen spiegeln die Antworten des FastAPI-Backends (backend/main.py) wider.
export type Sprache = "de" | "en" | "tr";
export type Buchstabe = "A" | "B" | "C" | "D";
export type Modus = "normal" | "daily";
export type JokerTyp = "5050" | "telefon" | "publikum" | "skip" | "doppel";

export interface StartAntwort {
  session_id: string;
  total: number;
  datum?: string;
}

export interface Frage {
  level: number;
  frage: string;
  antworten: Record<Buchstabe, string>;
  kategorie: string;
  schwierigkeit: number;
  sicher: boolean;
}

export interface AntwortErgebnis {
  richtig: boolean;
  zweiter_versuch?: boolean;
  richtige_antwort?: Buchstabe;
  richtige_antwort_text?: string;
  erklaerung?: string;
  iq?: number;
  iq_text?: string;
}

export type JokerErgebnis =
  | { typ: "5050"; entfernte: Buchstabe[] }
  | { typ: "telefon"; tipp: Buchstabe; text: string }
  | { typ: "publikum"; stimmen: Partial<Record<Buchstabe, number>> }
  | { typ: "skip" }
  | { typ: "doppel" };

export interface Highscore {
  name: string;
  iq: number;
  level: number;
}
