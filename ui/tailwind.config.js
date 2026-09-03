/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#0a0a0f',
        'bg-secondary': '#12121a',
        'bg-tertiary': '#1a1a24',
        'bg-elevated': '#222230',
        'accent-cyan': '#00d4ff',
        'severity-critical': '#ff3366',
        'severity-warning': '#ffaa33',
        'severity-success': '#33ff99',
        'text-primary': '#f0f0f5',
        'text-secondary': '#a0a0b0',
        'text-muted': '#6a6a7a',
        'border-subtle': '#2a2a3a',
      }
    },
  },
  plugins: [],
}
