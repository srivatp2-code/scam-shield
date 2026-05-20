/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontSize: {
        base: ["18px", "1.6"],
      },
    },
  },
  plugins: [],
};
