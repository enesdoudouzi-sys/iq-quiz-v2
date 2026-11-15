import { useState } from "react";
import type { Modus, Sprache } from "../api/types";
import type { TextSchluessel } from "../i18n";
import { nameGueltig } from "../quizLogik";

interface Props {
  t: (k: TextSchluessel) => string;
  sprache: Sprache;
  onSprache: (s: Sprache) => void;
  onStart: (name: string, modus: Modus) => void;
  onHighscores: () => void;
  laedt: boolean;
}

export function StartScreen({ t, sprache, onSprache, onStart, onHighscores, laedt }: Props) {
  const [name, setName] = useState("");
  const ok = nameGueltig(name) && !laedt;

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-center text-3xl font-bold">🧠 {t("titel")}</h1>
      <div className="flex gap-2">
        {(["de", "en", "tr"] as const).map((s) => (
          <button key={s} onClick={() => onSprache(s)}
            className={`flex-1 rounded-xl p-2 ${sprache === s ? "bg-accent" : "bg-card"}`}>
            {s.toUpperCase()}
          </button>
        ))}
      </div>
      <input
        className="rounded-xl bg-card p-3 outline-none ring-accent focus:ring-2"
        placeholder={t("name")} maxLength={20} value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <button disabled={!ok} onClick={() => onStart(name.trim(), "normal")}
        className="rounded-xl bg-ok p-3 font-bold text-bg disabled:opacity-40">
        {laedt ? t("laedt") : t("start")}
      </button>
      <button disabled={!ok} onClick={() => onStart(name.trim(), "daily")}
        className="rounded-xl bg-accent p-3 font-bold disabled:opacity-40">
        {t("daily")}
      </button>
      <button onClick={onHighscores} className="rounded-xl bg-card p-3">{t("bestenliste")}</button>
    </div>
  );
}
