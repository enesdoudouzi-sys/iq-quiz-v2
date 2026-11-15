import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { Highscore } from "../api/types";
import type { TextSchluessel } from "../i18n";

type Tab = "alle" | "woche" | "heute";

export function Bestenliste({ t, onZurueck }: { t: (k: TextSchluessel) => string; onZurueck: () => void }) {
  const [tab, setTab] = useState<Tab>("alle");
  const [liste, setListe] = useState<Highscore[] | null>(null);
  const [fehler, setFehler] = useState("");

  useEffect(() => {
    let aktuell = true; // verhindert, dass eine langsame alte Antwort die neue überschreibt
    setListe(null); setFehler("");
    const laden = tab === "heute" ? api.dailyHighscores() : api.highscores(tab);
    laden.then((l) => aktuell && setListe(l)).catch((e: Error) => aktuell && setFehler(e.message));
    return () => { aktuell = false; };
  }, [tab]);

  return (
    <div className="flex flex-col gap-3">
      <h2 className="text-2xl font-bold">{t("bestenliste")}</h2>
      <div className="flex gap-2">
        {(["alle", "woche", "heute"] as const).map((x) => (
          <button key={x} onClick={() => setTab(x)}
            className={`flex-1 rounded-xl p-2 text-sm ${tab === x ? "bg-accent" : "bg-card"}`}>
            {t(x)}
          </button>
        ))}
      </div>
      {fehler && <p className="text-bad">{fehler}</p>}
      {!liste && !fehler && <p>{t("laedt")}</p>}
      {liste?.length === 0 && <p className="text-gray-300">{t("leer")}</p>}
      <ol className="flex flex-col gap-2">
        {liste?.map((h, i) => (
          <li key={i} className="flex justify-between rounded-xl bg-card p-3">
            <span>{i + 1}. {h.name}</span>
            <b>IQ {h.iq}</b>
          </li>
        ))}
      </ol>
      <button onClick={onZurueck} className="rounded-xl bg-card p-3">{t("zurueck")}</button>
    </div>
  );
}
