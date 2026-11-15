import type { JokerTyp } from "../api/types";
import { ALLE_JOKER, JOKER_SYMBOL } from "../quizLogik";

interface Props {
  verfuegbar: Record<JokerTyp, boolean>;
  aktiv: boolean;
  onJoker: (typ: JokerTyp) => void;
}

export function JokerLeiste({ verfuegbar, aktiv, onJoker }: Props) {
  return (
    <div className="flex justify-between gap-2">
      {ALLE_JOKER.map((typ) => (
        <button key={typ} aria-label={`Joker ${typ}`}
          disabled={!aktiv || !verfuegbar[typ]} onClick={() => onJoker(typ)}
          className="flex-1 rounded-xl bg-card p-2 text-sm disabled:opacity-30">
          {JOKER_SYMBOL[typ]}
        </button>
      ))}
    </div>
  );
}
