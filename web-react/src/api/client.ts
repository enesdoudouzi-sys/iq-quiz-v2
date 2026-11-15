import type {
  AntwortErgebnis, Buchstabe, Frage, Highscore, JokerErgebnis, JokerTyp, Modus, Sprache, StartAntwort,
} from "./types";

// Lokal: VITE_API_URL=http://localhost:8000 npm run dev
export const API_URL: string = import.meta.env.VITE_API_URL ?? "https://iq-quiz-v2.onrender.com";

async function request<T>(pfad: string, init?: RequestInit): Promise<T> {
  const res = await fetch(API_URL + pfad, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers ?? {}) },
  });
  if (!res.ok) {
    // Server-Fehlermeldung (FastAPI: {"detail": "..."}) weiterreichen
    const body = await res.json().catch(() => ({}));
    throw new Error(typeof body.detail === "string" ? body.detail : `Fehler ${res.status}`);
  }
  return res.json() as Promise<T>;
}

const post = <T>(pfad: string, daten: unknown) =>
  request<T>(pfad, { method: "POST", body: JSON.stringify(daten) });

export const api = {
  start: (name: string, sprache: Sprache, modus: Modus) =>
    post<StartAntwort>(modus === "daily" ? "/api/daily/start" : "/api/start", { name, sprache }),

  frage: (sessionId: string, level: number) => request<Frage>(`/api/frage/${sessionId}/${level}`),

  antwort: (sessionId: string, level: number, antwort: Buchstabe) =>
    post<AntwortErgebnis>("/api/antwort", { session_id: sessionId, level, antwort }),

  joker: (sessionId: string, level: number, typ: JokerTyp, gesperrte: Buchstabe[]) =>
    post<JokerErgebnis>("/api/joker", { session_id: sessionId, level, typ, gesperrte }),

  highscores: (zeitraum: "alle" | "woche") => request<Highscore[]>(`/api/highscores?zeitraum=${zeitraum}`),
  dailyHighscores: () => request<Highscore[]>("/api/daily/highscores"),

  ergebnisSpeichern: (modus: Modus, sessionId: string, name: string, iq: number, level: number) =>
    post<{ ok: boolean }>(modus === "daily" ? "/api/daily/submit" : "/api/highscores",
      { session_id: sessionId, name, iq, level }),
};
