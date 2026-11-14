import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { Highscore } from "../api/types";

export function Bestenliste({ onZurueck }: { onZurueck: () => void }) {
  const [liste, setListe] = useState<Highscore[] | null>(null);
  const [fehler, setFehler] = useState("");

  useEffect(() => {
    api.highscores().then(setListe).catch((e: Error) => setFehler(e.message));
  }, []);

  return (
    <div className="flex flex-col gap-3">
      <h2 className="text-2xl font-bold">🏆 Bestenliste</h2>
      {fehler && <p className="text-bad">{fehler}</p>}
      {!liste && !fehler && <p>Lädt…</p>}
      <ol className="flex flex-col gap-2">
        {liste?.map((h, i) => (
          <li key={i} className="flex justify-between rounded-xl bg-card p-3">
            <span>{i + 1}. {h.name}</span>
            <b>IQ {h.iq}</b>
          </li>
        ))}
      </ol>
      <button onClick={onZurueck} className="rounded-xl bg-card p-3">Zurück</button>
    </div>
  );
}
