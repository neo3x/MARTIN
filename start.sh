#!/bin/bash
# Script de inicio rápido para M.A.R.T.I.N.

echo "🧠 Iniciando M.A.R.T.I.N..."

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias si es necesario
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    echo "📝 Por favor, edita el archivo .env con tus configuraciones"
    exit 1
fi

# Ejecutar M.A.R.T.I.N.
echo "🚀 Lanzando M.A.R.T.I.N..."
python main.py
