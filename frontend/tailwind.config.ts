/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx,mdx}",
  ],
  theme: {
    extend: {
      spacing: {
        68: '17rem',
      },
      colors: {
        primary: '#0ea5e9',      // Medical blue
        secondary: '#14b8a6',    // Teal
        accent: '#8b5cf6',       // Purple
        success: '#22c55e',
        warning: '#eab308',
        danger: '#ef4444',
        dark: '#1f2937',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
