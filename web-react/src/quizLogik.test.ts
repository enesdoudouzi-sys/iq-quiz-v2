import { describe, expect, it } from "vitest";
import { fortschritt, nameGueltig } from "./quizLogik";

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
