import { useEffect, useState } from "react";
import type { AntwortErgebnis, Buchstabe, Frage } from "../api/types";
import { fortschritt, SEKUNDEN_PRO_FRAGE } from "../quizLogik";

interface Props {
  frage: Frage;
  ergebnis: AntwortErgebnis | null;
  onAntwort: (b: Buchstabe) => void;
  onWeiter: () => void;
}

export function QuizScreen({ frage, ergebnis, onAntwort, onWeiter }: Props) {
  const [zeit, setZeit] = useState(SEKUNDEN_PRO_FRAGE);
  const [gewaehlt, setGewaehlt] = useState<Buchstabe | null>(null);

  // Neue Frage: Timer und Auswahl zurücksetzen
  useEffect(() => {
    setZeit(SEKUNDEN_PRO_FRAGE);
    setGewaehlt(null);
  }, [frage.level]);

  // Countdown; bei 0 zählt es als falsche Antwort ("A" als Platzhalter wird vom Server geprüft)
  useEffect(() => {
    if (ergebnis) return;
    if (zeit === 0) { onAntwort("A"); return; }
    const t = setTimeout(() => setZeit((z) => z - 1), 1000);
    return () => clearTimeout(t); // Aufräumen, sonst laufen mehrere Timer
  }, [zeit, ergebnis, onAntwort]);

  function farbe(b: Buchstabe): string {
    if (!ergebnis) return gewaehlt === b ? "bg-accent" : "bg-card";
    if (b === ergebnis.richtige_antwort) return "bg-ok text-bg";
    if (b === gewaehlt) return "bg-bad";
    return "bg-card opacity-60";
  }

  return (
    <div className="flex flex-col gap-3">
      <div className="h-2 rounded bg-card">
        <div className="h-2 rounded bg-accent" style={{ width: `${fortschritt(frage.level)}%` }} />
      </div>
      <div className="flex justify-between text-sm text-gray-300">
        <span>Frage {frage.level}/15 · {frage.kategorie}</span>
        <span className={zeit <= 5 ? "text-bad font-bold" : ""}>⏱ {zeit}s</span>
      </div>
      <p className="whitespace-pre-line rounded-xl bg-card p-4 text-lg">{frage.frage}</p>
      {(Object.keys(frage.antworten) as Buchstabe[]).map((b) => (
        <button
          key={b}
          disabled={!!ergebnis}
          onClick={() => { setGewaehlt(b); onAntwort(b); }}
          className={`rounded-xl p-3 text-left transition ${farbe(b)}`}
        >
          <b>{b}:</b> {frage.antworten[b]}
        </button>
      ))}
      {ergebnis && (
        <div className="rounded-xl bg-card p-3">
          <p className="font-bold">{ergebnis.richtig ? "✅ Richtig!" : "❌ Leider falsch"}</p>
          {ergebnis.erklaerung && <p className="text-sm text-gray-300">{ergebnis.erklaerung}</p>}
          <button onClick={onWeiter} className="mt-2 w-full rounded-xl bg-accent p-2">Weiter</button>
        </div>
      )}
    </div>
  );
}
