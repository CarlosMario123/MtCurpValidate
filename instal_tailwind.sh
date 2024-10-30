#!/bin/bash

# Crear el entorno del proyecto
echo "Instalando Tailwind CSS en el proyecto..."

# Iniciar un nuevo proyecto de Node.js (si package.json no existe)
if [[ ! -f "package.json" ]]; then
    echo "Inicializando npm en el proyecto..."
    npm init -y
fi

# Instalar Tailwind CSS y las dependencias requeridas
echo "Instalando Tailwind CSS y PostCSS..."
npm install -D tailwindcss postcss autoprefixer

# Crear el archivo de configuración de Tailwind CSS
echo "Generando archivo de configuración de Tailwind..."
npx tailwindcss init -p

# Configurar rutas de archivos para Tailwind en tailwind.config.js
echo "Configurando el archivo tailwind.config.js..."
cat > tailwind.config.js << EOL
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',     
    './static/**/*.js',          
    '*.css'        
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOL

# Crear la estructura básica de archivos CSS
echo "Creando archivo base para el CSS de Tailwind CSS..."

echo '@tailwind base;
@tailwind components;
@tailwind utilities;' > tailwind.css

# Compilar Tailwind CSS y generar el archivo de salida en static/css/tailwind.css para Flask
echo "Compilando Tailwind CSS..."
npx tailwindcss -i tailwind.css -o static/css/tailwind.css --watch 

echo "Instalación completada. Tailwind CSS está configurado y listo para usarse en tu proyecto Flask."

