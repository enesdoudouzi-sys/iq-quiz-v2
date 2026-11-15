import { describe, expect, it } from "vitest";
import { fortschritt, nameGueltig, spielVorbei, waehlbar } from "./quizLogik";

describe("fortschritt", () => {
  it("startet bei 0 %", () => expect(fortschritt(1)).toBe(0));
  it("ist nach der Hälfte ca. 47 %", () => expect(fortschritt(8)).toBe(47));
});

describe("nameGueltig", () => {
  it("akzeptiert normale Namen", () => expect(nameGueltig("Enes")).toBe(true));
  it("lehnt leere Namen ab", () => expect(nameGueltig("   ")).toBe(false));
  it("lehnt HTML ab", () => expect(nameGueltig("<script>")).toBe(false));
  it("lehnt zu lange Namen ab", () => expect(nameGueltig("x".repeat(21))).toBe(false));
});

describe("spielVorbei", () => {
  it("falsche Antwort beendet das Spiel", () => expect(spielVorbei(false, 3)).toBe(true));
  it("richtige Antwort geht weiter", () => expect(spielVorbei(true, 3)).toBe(false));
  it("nach Frage 15 ist Schluss", () => expect(spielVorbei(true, 15)).toBe(true));
});

describe("waehlbar", () => {
  it("entfernt 50:50- und gesperrte Antworten", () =>
    expect(waehlbar(["A", "B", "C", "D"], ["B", "D"], ["A"])).toEqual(["C"]));
});
