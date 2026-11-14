/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: { bg: "#060614", card: "#11112a", accent: "#7c5cff", ok: "#3ddc84", bad: "#ff5c7a" },
    },
  },
  plugins: [],
};
