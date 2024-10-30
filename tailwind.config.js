/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',     
    './static/**/*.js',          
    '*.css'         
  ],
  theme: {
    extend: {
      colors: {
        'custom-maroon': '#641635',
        'custom-gold': '#a47e2c',
        'custom-lightblue': '#dbe9f0',
      },
    },
  },
  plugins: [],
}
