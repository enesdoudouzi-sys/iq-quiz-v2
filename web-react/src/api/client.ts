import type { AntwortErgebnis, Buchstabe, Frage, Highscore, Sprache, StartAntwort } from "./types";

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

export const api = {
  start: (name: string, sprache: Sprache) =>
    request<StartAntwort>("/api/start", { method: "POST", body: JSON.stringify({ name, sprache }) }),

  frage: (sessionId: string, level: number) =>
    request<Frage>(`/api/frage/${sessionId}/${level}`),

  antwort: (sessionId: string, level: number, antwort: Buchstabe) =>
    request<AntwortErgebnis>("/api/antwort", {
      method: "POST",
      body: JSON.stringify({ session_id: sessionId, level, antwort }),
    }),

  highscores: () => request<Highscore[]>("/api/highscores"),

  highscoreSpeichern: (sessionId: string, name: string, iq: number, level: number) =>
    request<{ ok: boolean }>("/api/highscores", {
      method: "POST",
      body: JSON.stringify({ session_id: sessionId, name, iq, level }),
    }),
};
