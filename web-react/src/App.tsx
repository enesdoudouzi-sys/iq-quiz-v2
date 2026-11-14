import { useCallback, useState } from "react";
import { api } from "./api/client";
import type { AntwortErgebnis, Buchstabe, Frage, Sprache } from "./api/types";
import { ANZAHL_FRAGEN } from "./quizLogik";
import { StartScreen } from "./components/StartScreen";
import { QuizScreen } from "./components/QuizScreen";
import { ErgebnisScreen } from "./components/ErgebnisScreen";
import { Bestenliste } from "./components/Bestenliste";

type Ansicht = "start" | "quiz" | "ergebnis" | "bestenliste";

export default function App() {
  const [ansicht, setAnsicht] = useState<Ansicht>("start");
  const [sessionId, setSessionId] = useState("");
  const [name, setName] = useState("");
  const [frage, setFrage] = useState<Frage | null>(null);
  const [ergebnis, setErgebnis] = useState<AntwortErgebnis | null>(null);
  const [iq, setIq] = useState({ wert: 85, text: "" });
  const [gespeichert, setGespeichert] = useState(false);
  const [laedt, setLaedt] = useState(false);
  const [fehler, setFehler] = useState("");

  async function starten(n: string, sprache: Sprache) {
    setLaedt(true); setFehler("");
    try {
      const s = await api.start(n, sprache);
      setSessionId(s.session_id); setName(n); setGespeichert(false);
      setFrage(await api.frage(s.session_id, 1));
      setErgebnis(null);
      setAnsicht("quiz");
    } catch (e) {
      setFehler((e as Error).message);
    } finally {
      setLaedt(false);
    }
  }

  // useCallback: gleiche Funktion bei jedem Rendern, damit der Timer-Effekt nicht neu startet
  const antworten = useCallback(async (b: Buchstabe) => {
    if (!frage) return;
    try {
      const r = await api.antwort(sessionId, frage.level, b);
      setErgebnis(r);
      if (r.iq) setIq({ wert: r.iq, text: r.iq_text ?? "" });
    } catch (e) {
      setFehler((e as Error).message);
    }
  }, [frage, sessionId]);

  async function weiter() {
    if (!frage || !ergebnis) return;
    if (!ergebnis.richtig || frage.level >= ANZAHL_FRAGEN) {
      setAnsicht("ergebnis");
      return;
    }
    setFrage(await api.frage(sessionId, frage.level + 1));
    setErgebnis(null);
  }

  async function speichern() {
    try {
      await api.highscoreSpeichern(sessionId, name, iq.wert, frage?.level ?? 0);
      setGespeichert(true);
    } catch (e) {
      setFehler((e as Error).message);
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center p-4">
      {fehler && <p className="mb-3 rounded-xl bg-bad/20 p-3 text-bad">{fehler}</p>}
      {ansicht === "start" && (
        <StartScreen onStart={starten} onHighscores={() => setAnsicht("bestenliste")} laedt={laedt} />
      )}
      {ansicht === "quiz" && frage && (
        <QuizScreen frage={frage} ergebnis={ergebnis} onAntwort={antworten} onWeiter={weiter} />
      )}
      {ansicht === "ergebnis" && (
        <ErgebnisScreen iq={iq.wert} iqText={iq.text} gespeichert={gespeichert}
          onSpeichern={speichern} onNeu={() => setAnsicht("start")} />
      )}
      {ansicht === "bestenliste" && <Bestenliste onZurueck={() => setAnsicht("start")} />}
    </main>
  );
}
