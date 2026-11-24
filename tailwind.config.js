/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./layouts/**/*.html', './assets/js/**/*.js', './content/**/*.md'],
  theme: {
    extend: {
      // Palette lives in assets/css/main.css (:root, RGB triplets) so there is ONE place with raw values.
      colors: {
        primary: 'rgb(var(--primary) / <alpha-value>)',             // deep forest — brand, headings, buttons
        'primary-dark': 'rgb(var(--primary-dark) / <alpha-value>)', // hover states, deep sections
        secondary: 'rgb(var(--secondary) / <alpha-value>)',         // moss / olive (AA on sand)
        accent: 'rgb(var(--accent) / <alpha-value>)',               // warm amber — highlights
        'accent-light': 'rgb(var(--accent-light) / <alpha-value>)', // amber hover
        surface: 'rgb(var(--surface) / <alpha-value>)',             // warm sand
        'surface-light': 'rgb(var(--surface-light) / <alpha-value>)',
        'surface-deep': 'rgb(var(--surface-deep) / <alpha-value>)',
        'surface-dark': 'rgb(var(--surface-dark) / <alpha-value>)', // dark canopy
        muted: 'rgb(var(--muted) / <alpha-value>)',                 // captions (AA on sand)
      },
      fontFamily: {
        heading: ['Montserrat', 'sans-serif'],
        body: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
      },
      borderRadius: {
        organic: '40% 60% 55% 45% / 45% 55% 60% 40%',
        wave: '0 0 50% 50% / 0 0 20px 20px',
        leaf: '0 70% 0 70%',
        petal: '60% 0 60% 0',
      },
      boxShadow: {
        botanical: '0 20px 50px -20px rgb(var(--primary-dark) / .45)',
        glow: '0 0 60px -10px rgb(var(--accent) / .55)',
      },
    },
  },
  plugins: [],
}
