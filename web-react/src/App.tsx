import { useCallback, useMemo, useState } from "react";
import { api } from "./api/client";
import type { AntwortErgebnis, Buchstabe, Frage, JokerErgebnis, JokerTyp, Modus, Sprache } from "./api/types";
import { gespeicherteSprache, spracheMerken, texte } from "./i18n";
import { ANZAHL_FRAGEN, spielVorbei } from "./quizLogik";
import { StartScreen } from "./components/StartScreen";
import { QuizScreen } from "./components/QuizScreen";
import { ErgebnisScreen } from "./components/ErgebnisScreen";
import { Bestenliste } from "./components/Bestenliste";

type Ansicht = "start" | "quiz" | "ergebnis" | "bestenliste";
const ALLE_JOKER_FREI: Record<JokerTyp, boolean> = { "5050": true, telefon: true, publikum: true, skip: true, doppel: true };

export default function App() {
  const [sprache, setSprache] = useState<Sprache>(gespeicherteSprache);
  const t = useMemo(() => texte(sprache), [sprache]);

  const [ansicht, setAnsicht] = useState<Ansicht>("start");
  const [modus, setModus] = useState<Modus>("normal");
  const [sessionId, setSessionId] = useState("");
  const [name, setName] = useState("");
  const [frage, setFrage] = useState<Frage | null>(null);
  const [ergebnis, setErgebnis] = useState<AntwortErgebnis | null>(null);
  const [zeitAus, setZeitAus] = useState(false);
  const [joker, setJoker] = useState(ALLE_JOKER_FREI);
  const [hinweis, setHinweis] = useState<JokerErgebnis | null>(null);
  const [entfernt, setEntfernt] = useState<Buchstabe[]>([]);
  const [gesperrt, setGesperrt] = useState<Buchstabe[]>([]);
  const [iq, setIq] = useState({ wert: 85, text: "" });
  const [gespeichert, setGespeichert] = useState(false);
  const [laedt, setLaedt] = useState(false);
  const [fehler, setFehler] = useState("");

  const fehlerZeigen = (e: unknown) => setFehler((e as Error).message);

  function spracheWechseln(s: Sprache) { setSprache(s); spracheMerken(s); }

  /** Frage für ein Level laden und alle Anzeigen für die neue Frage zurücksetzen. */
  async function frageLaden(sid: string, level: number) {
    setFrage(await api.frage(sid, level));
    setErgebnis(null); setZeitAus(false); setHinweis(null); setEntfernt([]); setGesperrt([]);
  }

  async function starten(n: string, m: Modus) {
    setLaedt(true); setFehler("");
    try {
      const s = await api.start(n, sprache, m);
      setSessionId(s.session_id); setName(n); setModus(m);
      setJoker(ALLE_JOKER_FREI); setIq({ wert: 85, text: "" }); setGespeichert(false);
      await frageLaden(s.session_id, 1);
      setAnsicht("quiz");
    } catch (e) { fehlerZeigen(e); } finally { setLaedt(false); }
  }

  async function antworten(b: Buchstabe) {
    if (!frage) return;
    try {
      const r = await api.antwort(sessionId, frage.level, b);
      if (r.zweiter_versuch) { setGesperrt((g) => [...g, b]); return; } // Doppelte Chance
      setErgebnis(r);
      if (r.iq) setIq({ wert: r.iq, text: r.iq_text ?? "" });
    } catch (e) { fehlerZeigen(e); }
  }

  async function jokerNutzen(typ: JokerTyp) {
    if (!frage) return;
    try {
      const r = await api.joker(sessionId, frage.level, typ, [...entfernt, ...gesperrt]);
      setJoker((j) => ({ ...j, [typ]: false }));
      if (r.typ === "5050") setEntfernt(r.entfernte);
      else if (r.typ === "skip") {
        if (frage.level >= ANZAHL_FRAGEN) setAnsicht("ergebnis");
        else await frageLaden(sessionId, frage.level + 1);
      } else setHinweis(r);
    } catch (e) { fehlerZeigen(e); }
  }

  // useCallback: gleiche Funktion bei jedem Rendern, damit der Timer-Effekt nicht neu startet
  const zeitAbgelaufen = useCallback(() => setZeitAus(true), []);

  async function weiter() {
    if (!frage) return;
    if (zeitAus || !ergebnis || spielVorbei(ergebnis.richtig, frage.level)) { setAnsicht("ergebnis"); return; }
    try { await frageLaden(sessionId, frage.level + 1); } catch (e) { fehlerZeigen(e); }
  }

  async function speichern() {
    try {
      await api.ergebnisSpeichern(modus, sessionId, name, iq.wert, frage?.level ?? 0);
      setGespeichert(true);
    } catch (e) { fehlerZeigen(e); }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center p-4">
      {fehler && <p role="alert" className="mb-3 rounded-xl bg-bad/20 p-3 text-bad">{fehler}</p>}
      {ansicht === "start" && (
        <StartScreen t={t} sprache={sprache} onSprache={spracheWechseln} onStart={starten}
          onHighscores={() => setAnsicht("bestenliste")} laedt={laedt} />
      )}
      {ansicht === "quiz" && frage && (
        <QuizScreen t={t} frage={frage} ergebnis={ergebnis} zeitAus={zeitAus} joker={joker}
          jokerHinweis={hinweis} entfernt={entfernt} gesperrt={gesperrt}
          onAntwort={antworten} onJoker={jokerNutzen} onZeitAus={zeitAbgelaufen} onWeiter={weiter} />
      )}
      {ansicht === "ergebnis" && (
        <ErgebnisScreen t={t} iq={iq.wert} iqText={iq.text} gespeichert={gespeichert}
          onSpeichern={speichern} onNeu={() => setAnsicht("start")} />
      )}
      {ansicht === "bestenliste" && <Bestenliste t={t} onZurueck={() => setAnsicht("start")} />}
    </main>
  );
}
