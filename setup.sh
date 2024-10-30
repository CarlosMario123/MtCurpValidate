#!/bin/bash

# Nombre del entorno virtual
ENV_DIR="venv"

# Verificar si python3.12-venv está instalado en el sistema
if ! dpkg -s python3.12-venv &> /dev/null; then
    echo "python3.12-venv no está instalado. Instalándolo ahora..."
    sudo apt update
    sudo apt install python3.12-venv -y
fi

# Crear el entorno virtual en el directorio especificado
echo "Creando el entorno virtual en el directorio $ENV_DIR..."
python3.12 -m venv $ENV_DIR

# Verificar si la creación del entorno virtual fue exitosa
if [[ ! -d "$ENV_DIR" ]]; then
    echo "Error: No se pudo crear el entorno virtual. Revisa la instalación de python3.12-venv."
    exit 1
fi

# Activar el entorno virtual
echo "Activando el entorno virtual..."
source $ENV_DIR/bin/activate

# Verificar si la activación fue exitosa
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Entorno virtual activado exitosamente."
else
    echo "Error: No se pudo activar el entorno virtual."
    exit 1
fi

# Instalar dependencias dentro del entorno virtual
if [[ -f "requirements.txt" ]]; then
    echo "Instalando dependencias desde requirements.txt en el entorno virtual..."
    pip install -r requirements.txt
else
    echo "No se encontró requirements.txt. Instalando dependencias básicas en el entorno virtual..."
    pip install requests flask
fi

# Confirmación de finalización
echo "Entorno virtual creado y dependencias instaladas exitosamente en el entorno virtual."
echo "Para activar el entorno virtual en el futuro, ejecuta: source $ENV_DIR/bin/activate"

# Desactivar el entorno virtual para finalizar el script
deactivate
