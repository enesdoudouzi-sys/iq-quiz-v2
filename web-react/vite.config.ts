import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "./", // relative Pfade: funktioniert auf GitHub Pages, itch.io und in Capacitor
});
