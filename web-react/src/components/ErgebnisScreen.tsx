import type { TextSchluessel } from "../i18n";

interface Props {
  t: (k: TextSchluessel) => string;
  iq: number;
  iqText: string;
  gespeichert: boolean;
  onSpeichern: () => void;
  onNeu: () => void;
}

export function ErgebnisScreen({ t, iq, iqText, gespeichert, onSpeichern, onNeu }: Props) {
  return (
    <div className="flex flex-col items-center gap-4 text-center">
      <p className="text-gray-300">{t("ergebnis")}</p>
      <p className="text-6xl font-bold text-accent" data-testid="iq">{iq}</p>
      {iqText && <p className="text-xl">{iqText}</p>}
      <button disabled={gespeichert} onClick={onSpeichern}
        className="w-full rounded-xl bg-ok p-3 font-bold text-bg disabled:opacity-40">
        {gespeichert ? t("gespeichert") : t("eintragen")}
      </button>
      <button onClick={onNeu} className="w-full rounded-xl bg-card p-3">{t("neu")}</button>
    </div>
  );
}
