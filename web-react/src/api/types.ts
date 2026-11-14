// Typen spiegeln die Antworten des FastAPI-Backends (backend/main.py) wider.
export type Sprache = "de" | "en" | "tr";
export type Buchstabe = "A" | "B" | "C" | "D";

export interface StartAntwort {
  session_id: string;
  total: number;
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

export interface Highscore {
  name: string;
  iq: number;
  level: number;
}
