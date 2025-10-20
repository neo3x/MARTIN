#!/bin/bash

# ================================================
# Script de configuración para M.A.R.T.I.N.
# Modular Assistant for Reasoning, Tactics, Inference and Navigation
# ================================================

echo "🧠 Configurando estructura de directorios para M.A.R.T.I.N..."
echo "================================================"

# Crear directorio principal si no existe
PROJECT_NAME="MARTIN"
if [ ! -d "$PROJECT_NAME" ]; then
    echo "📁 Creando directorio principal: $PROJECT_NAME"
    mkdir "$PROJECT_NAME"
fi

cd "$PROJECT_NAME"

# Crear estructura de directorios según el README
echo "📂 Creando estructura de carpetas..."

# Directorio del núcleo lógico del agente
mkdir -p agent_core
echo "  ✓ /agent_core - Núcleo lógico (razonamiento, planificación)"

# Directorio de herramientas externas
mkdir -p tools
echo "  ✓ /tools - Módulos integrables externos"

# Directorio de memoria y contexto
mkdir -p memory
echo "  ✓ /memory - Adaptadores de memoria y almacenamiento"

# Directorio de interfaces
mkdir -p interface
echo "  ✓ /interface - Gradio/CLI/REST endpoints"

# Directorio de configuraciones
mkdir -p configs
echo "  ✓ /configs - Parámetros y prompts del agente"

# Directorio de documentación
mkdir -p docs
echo "  ✓ /docs - Documentación y casos de uso"

# Crear subdirectorios adicionales útiles
echo ""
echo "📂 Creando subdirectorios adicionales..."

# Subdirectorios para agent_core
mkdir -p agent_core/reasoning
mkdir -p agent_core/planning
mkdir -p agent_core/execution
echo "  ✓ Subdirectorios de agent_core creados"

# Subdirectorios para tools
mkdir -p tools/web_search
mkdir -p tools/file_parsers
mkdir -p tools/apis
echo "  ✓ Subdirectorios de tools creados"

# Subdirectorios para memory
mkdir -p memory/short_term
mkdir -p memory/long_term
mkdir -p memory/cache
echo "  ✓ Subdirectorios de memory creados"

# Subdirectorios para interface
mkdir -p interface/cli
mkdir -p interface/gradio
mkdir -p interface/api
echo "  ✓ Subdirectorios de interface creados"

# Subdirectorios para docs
mkdir -p docs/diagrams
mkdir -p docs/use_cases
mkdir -p docs/api_reference
echo "  ✓ Subdirectorios de docs creados"

# Crear archivos base necesarios
echo ""
echo "📄 Creando archivos base..."

# Crear archivo principal
touch main.py
echo "  ✓ main.py creado"

# Crear archivos __init__.py para convertir directorios en paquetes Python
find . -type d -name "*.pyc" -prune -o -type d -exec touch {}/__init__.py \; 2>/dev/null
echo "  ✓ Archivos __init__.py creados en todos los directorios"

# Crear archivos de configuración base
touch configs/config.yaml
touch configs/prompts.yaml
echo "  ✓ Archivos de configuración base creados"

# Crear requirements.txt
cat > requirements.txt << EOF
# Core dependencies for M.A.R.T.I.N.
gradio>=4.0.0
openai>=1.0.0
langchain>=0.1.0
pyyaml>=6.0
python-dotenv>=1.0.0
requests>=2.31.0
numpy>=1.24.0
pandas>=2.0.0
EOF
echo "  ✓ requirements.txt creado"

# Crear .env.example
cat > .env.example << EOF
# Environment variables for M.A.R.T.I.N.
# Copy this file to .env and fill in your values

# LLM Configuration
OPENAI_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7

# Agent Configuration
AGENT_MODE=direct  # Options: passive, direct, safe
AGENT_VERBOSE=true

# Memory Configuration
MEMORY_TYPE=local  # Options: local, redis, postgresql
MEMORY_PATH=./memory/storage

# Interface Configuration
INTERFACE_TYPE=gradio  # Options: cli, gradio, api
INTERFACE_PORT=7860
EOF
echo "  ✓ .env.example creado"

# Crear .gitignore
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Memory and cache
memory/storage/
memory/cache/
*.db
*.sqlite

# Logs
logs/
*.log

# Temporary files
tmp/
temp/
*.tmp
EOF
echo "  ✓ .gitignore creado"

# Mover el README.md si existe en el directorio padre
if [ -f ../README.md ]; then
    cp ../README.md .
    echo "  ✓ README.md copiado"
fi

# Crear un script de inicio rápido
cat > start.sh << 'EOF'
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
EOF
chmod +x start.sh
echo "  ✓ start.sh creado y configurado como ejecutable"

echo ""
echo "================================================"
echo "✅ ¡Estructura de M.A.R.T.I.N. creada exitosamente!"
echo ""
echo "📍 Ubicación del proyecto: $(pwd)"
echo ""
echo "🚀 Próximos pasos:"
echo "   1. cd $PROJECT_NAME"
echo "   2. Copia .env.example a .env y configura tus variables"
echo "   3. Instala las dependencias: pip install -r requirements.txt"
echo "   4. Ejecuta: ./start.sh o python main.py"
echo ""
echo "📚 Estructura creada:"
tree -L 2 2>/dev/null || ls -la
echo "================================================"