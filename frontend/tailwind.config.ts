import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        // Halliburton Brand Colors
        halliburton: {
          red: '#E31837',
          'red-dark': '#B91329',
          'red-light': '#FF4D6A',
          'dark-gray': '#2C2C2C',
          'medium-gray': '#5A5A5A',
          'light-gray': '#F5F5F5',
          blue: '#0066CC',
          'blue-dark': '#004C99',
          orange: '#FF6B35',
        },
        primary: {
          50: '#FEE2E7',
          100: '#FCC5CF',
          200: '#FA8B9F',
          300: '#F7516F',
          400: '#F5173F',
          500: '#E31837', // Halliburton Red
          600: '#B91329',
          700: '#8F0E1F',
          800: '#650A16',
          900: '#3B050C',
        },
      },
      fontFamily: {
        sans: ['Inter', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
  darkMode: 'class',
};

export default config;

