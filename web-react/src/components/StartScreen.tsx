import { useState } from "react";
import type { Sprache } from "../api/types";
import { nameGueltig } from "../quizLogik";

interface Props {
  onStart: (name: string, sprache: Sprache) => void;
  onHighscores: () => void;
  laedt: boolean;
}

export function StartScreen({ onStart, onHighscores, laedt }: Props) {
  const [name, setName] = useState("");
  const [sprache, setSprache] = useState<Sprache>("de");

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-3xl font-bold text-center">🧠 IQ Quiz</h1>
      <input
        className="rounded-xl bg-card p-3 outline-none ring-accent focus:ring-2"
        placeholder="Dein Name"
        maxLength={20}
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <div className="flex gap-2">
        {(["de", "en", "tr"] as const).map((s) => (
          <button
            key={s}
            onClick={() => setSprache(s)}
            className={`flex-1 rounded-xl p-2 ${sprache === s ? "bg-accent" : "bg-card"}`}
          >
            {s.toUpperCase()}
          </button>
        ))}
      </div>
      <button
        disabled={!nameGueltig(name) || laedt}
        onClick={() => onStart(name.trim(), sprache)}
        className="rounded-xl bg-ok p-3 font-bold text-bg disabled:opacity-40"
      >
        {laedt ? "Lädt…" : "Quiz starten"}
      </button>
      <button onClick={onHighscores} className="rounded-xl bg-card p-3">🏆 Bestenliste</button>
    </div>
  );
}
