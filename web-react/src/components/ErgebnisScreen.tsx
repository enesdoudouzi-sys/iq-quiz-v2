interface Props {
  iq: number;
  iqText: string;
  gespeichert: boolean;
  onSpeichern: () => void;
  onNeu: () => void;
}

export function ErgebnisScreen({ iq, iqText, gespeichert, onSpeichern, onNeu }: Props) {
  return (
    <div className="flex flex-col items-center gap-4 text-center">
      <p className="text-gray-300">Dein Ergebnis</p>
      <p className="text-6xl font-bold text-accent">{iq}</p>
      <p className="text-xl">{iqText}</p>
      <button
        disabled={gespeichert}
        onClick={onSpeichern}
        className="w-full rounded-xl bg-ok p-3 font-bold text-bg disabled:opacity-40"
      >
        {gespeichert ? "✔ Gespeichert" : "In Bestenliste eintragen"}
      </button>
      <button onClick={onNeu} className="w-full rounded-xl bg-card p-3">Nochmal spielen</button>
    </div>
  );
}
