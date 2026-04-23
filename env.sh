#!/bin/bash
# Script para preparar entorno Python y dependencias
set -e

# Nombre del entorno virtual
VENV_DIR=".venv"

# Crear entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
	echo "Creando entorno virtual en $VENV_DIR..."
	python3.12 -m venv "$VENV_DIR"
fi

# Activar entorno virtual
source "$VENV_DIR/bin/activate"
echo "Entorno virtual activado."

# Instalar dependencias
if [ -f requirements.txt ]; then
	echo "Instalando dependencias de requirements.txt..."
	pip install --upgrade pip
	pip install -r requirements.txt
else
	echo "No se encontró requirements.txt."
fi

export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/sbc-contentextraction-ca193c757897.json"

echo "Entorno listo para ejecutar el código."
