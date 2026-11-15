import { useEffect, useState } from "react";
import type { AntwortErgebnis, Buchstabe, Frage, JokerErgebnis, JokerTyp } from "../api/types";
import type { TextSchluessel } from "../i18n";
import { fortschritt, SEKUNDEN_PRO_FRAGE } from "../quizLogik";
import { JokerLeiste } from "./JokerLeiste";

interface Props {
  t: (k: TextSchluessel) => string;
  frage: Frage;
  ergebnis: AntwortErgebnis | null;
  zeitAus: boolean;
  joker: Record<JokerTyp, boolean>;
  jokerHinweis: JokerErgebnis | null;
  entfernt: Buchstabe[];   // durch 50:50 entfernt
  gesperrt: Buchstabe[];   // bei "Doppelte Chance" schon falsch geraten
  onAntwort: (b: Buchstabe) => void;
  onJoker: (typ: JokerTyp) => void;
  onZeitAus: () => void;
  onWeiter: () => void;
}

export function QuizScreen(p: Props) {
  const { t, frage, ergebnis, zeitAus } = p;
  const [zeit, setZeit] = useState(SEKUNDEN_PRO_FRAGE);
  const [gewaehlt, setGewaehlt] = useState<Buchstabe | null>(null);
  const beantwortet = !!ergebnis || zeitAus;

  // Neue Frage: Timer und Auswahl zurücksetzen
  useEffect(() => { setZeit(SEKUNDEN_PRO_FRAGE); setGewaehlt(null); }, [frage.level]);

  // Countdown. Bei 0 endet das Spiel (wie in der Original-App, ohne Antwort an den Server)
  const { onZeitAus } = p;
  useEffect(() => {
    if (beantwortet) return;
    if (zeit === 0) { onZeitAus(); return; }
    const timer = setTimeout(() => setZeit((z) => z - 1), 1000);
    return () => clearTimeout(timer); // Aufräumen, sonst laufen mehrere Timer parallel
  }, [zeit, beantwortet, onZeitAus]);

  function farbe(b: Buchstabe): string {
    if (p.entfernt.includes(b)) return "invisible";
    if (p.gesperrt.includes(b)) return "bg-bad/40 line-through";
    if (!ergebnis) return gewaehlt === b ? "bg-accent" : "bg-card";
    if (b === ergebnis.richtige_antwort) return "bg-ok text-bg";
    if (b === gewaehlt) return "bg-bad";
    return "bg-card opacity-60";
  }

  const hinweis = p.jokerHinweis;
  return (
    <div className="flex flex-col gap-3">
      <div className="h-2 rounded bg-card">
        <div className="h-2 rounded bg-accent transition-all" style={{ width: `${fortschritt(frage.level)}%` }} />
      </div>
      <div className="flex justify-between text-sm text-gray-300">
        <span>{t("frage")} {frage.level}/15 · {frage.kategorie}</span>
        <span className={zeit <= 5 ? "font-bold text-bad" : ""}>⏱ {zeit}s</span>
      </div>
      <JokerLeiste verfuegbar={p.joker} aktiv={!beantwortet} onJoker={p.onJoker} />
      <p className="whitespace-pre-line rounded-xl bg-card p-4 text-lg">{frage.frage}</p>

      {hinweis?.typ === "telefon" && (
        <p className="rounded-xl bg-card p-3 text-sm">📞 {t("telefon")} <b>{hinweis.tipp}</b></p>
      )}
      {hinweis?.typ === "publikum" && (
        <div className="rounded-xl bg-card p-3 text-sm">
          <p className="mb-1">👥 {t("publikum")}</p>
          {(Object.entries(hinweis.stimmen) as [Buchstabe, number][]).map(([b, pz]) => (
            <div key={b} className="flex items-center gap-2">
              <span className="w-4">{b}</span>
              <div className="h-2 rounded bg-accent" style={{ width: `${pz}%` }} />
              <span>{pz}%</span>
            </div>
          ))}
        </div>
      )}

      {(Object.keys(frage.antworten) as Buchstabe[]).map((b) => (
        <button key={b}
          disabled={beantwortet || p.entfernt.includes(b) || p.gesperrt.includes(b)}
          onClick={() => { setGewaehlt(b); p.onAntwort(b); }}
          className={`rounded-xl p-3 text-left transition ${farbe(b)}`}>
          <b>{b}:</b> {frage.antworten[b]}
        </button>
      ))}

      {beantwortet && (
        <div className="rounded-xl bg-card p-3">
          <p className="font-bold">{zeitAus ? t("zeitAus") : ergebnis?.richtig ? t("richtig") : t("falsch")}</p>
          {ergebnis?.erklaerung && <p className="text-sm text-gray-300">{ergebnis.erklaerung}</p>}
          <button onClick={p.onWeiter} className="mt-2 w-full rounded-xl bg-accent p-2">{t("weiter")}</button>
        </div>
      )}
    </div>
  );
}
