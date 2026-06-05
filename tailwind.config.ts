import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Georgia', 'serif'],
      },
      colors: {
        cream: '#FAF7F2',
        blush: '#F2D4C8',
        sage: '#A8B5A0',
        charcoal: '#2C2C2C',
        warm: '#8B6F5E',
      },
    },
  },
  plugins: [],
}

export default config
