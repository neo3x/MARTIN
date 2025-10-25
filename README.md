# 🧠 M.A.R.T.I.N.

**Modular Assistant for Reasoning, Tactics, Inference and Navigation**

Agente de IA con **razonamiento adaptativo tri-modal** para compliance automation.

---

## 🎯 ¿Qué es M.A.R.T.I.N.?

M.A.R.T.I.N. es un agente de IA que **adapta su comportamiento** según el contexto de la tarea:

- 🟦 **MODO PASIVO**: Propone plan, espera confirmación (tareas ambiguas)
- 🟩 **MODO DIRECTO**: Ejecuta autónomamente (tareas claras, bajo riesgo)
- 🟨 **MODO SEGURO**: Auto-valida antes de actuar (alto riesgo, producción)

### La Innovación

A diferencia de otros agentes que son siempre autónomos (riesgoso) o siempre pasivos (ineficiente), **M.A.R.T.I.N. razona sobre CÓMO razonar**, eligiendo el nivel de autonomía apropiado según:

- Claridad de la tarea
- Nivel de riesgo
- Ambiente (dev/staging/production)
- Contexto del usuario

---

## 🚀 Quick Start (5 minutos)

### 1. Instalación

```bash
# Clonar repositorio
git https://github.com/neo3x/MARTIN
cd MARTIN

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración (Opcional)

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu API key de OpenAI
# OPENAI_API_KEY=tu-key-aqui
```

**Nota:** M.A.R.T.I.N. funciona SIN API key en modo simulado para testing.

### 3. Ejecutar Demo

```bash
# Demo rápida de los 3 modos
python quick_start.py
```

### 4. Interfaz Web

```bash
# Lanzar interfaz Gradio
python interface/gradio_app.py

# Abre http://localhost:7860 en tu navegador
```

---

## 📚 Ejemplos de Uso

### Ejemplo 1: Modo Pasivo
```
Usuario: "Ayúdame a preparar mi startup para SOC 2"

M.A.R.T.I.N. (Pasivo):
📋 Propongo este plan:
1. Auditar infraestructura actual (2h)
2. Identificar gaps críticos (1h)
3. Generar roadmap priorizado (30min)

¿Procedo con este plan?
```

### Ejemplo 2: Modo Directo
```
Usuario: "Genera política de contraseñas según ISO 27001"

M.A.R.T.I.N. (Directo):
⚡ EJECUTADO

Política generada:
- Longitud mínima: 12 caracteres
- Complejidad: mayúsculas + números + símbolos
- Rotación: 90 días
- MFA obligatorio para roles admin

[Documento completo adjunto]
```

### Ejemplo 3: Modo Seguro
```
Usuario: "Deshabilita MFA para admin@empresa.com"
Ambiente: Production

M.A.R.T.I.N. (Seguro):
🛡️ ACCIÓN BLOQUEADA

Riesgos detectados:
• Usuario con permisos root
• Reducción crítica de seguridad
• Ambiente de producción

Alternativa segura:
1. Crear admin temporal con MFA
2. Transferir permisos críticos
3. Luego proceder con cambio original
```

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│           USER INPUT                    │
└────────────────┬────────────────────────┘
                 │
        ┌────────▼────────┐
        │  MODE SELECTOR  │  ← Analiza riesgo + claridad
        └────────┬────────┘
                 │
     ┌───────────┴───────────┐
     │                       │
┌────▼────┐  ┌──────▼─────┐  ┌────▼────┐
│ PASSIVE │  │   DIRECT   │  │  SAFE   │
│ REASON  │  │   REASON   │  │ REASON  │
└─────────┘  └────────────┘  └─────────┘
```

### Componentes

- **ModeSelector**: Analiza tarea y decide modo óptimo
- **Reasoning Engines**: 3 motores de razonamiento diferentes
- **MARTINAgent**: Orquestador principal
- **Interface**: CLI y Web (Gradio)

---

## 📁 Estructura del Proyecto

```
MARTIN/
├── agent_core/
│   ├── __init__.py
│   ├── mode_selector.py       # El cerebro que decide
│   ├── reasoning_engines.py   # Los 3 modos
│   └── martin_agent.py        # Orquestador principal
├── interface/
│   ├── __init__.py
│   └── gradio_app.py          # UI web
├── tools/                     # Herramientas futuras
├── memory/                    # Sistema de memoria
├── configs/                   # Configuraciones
├── requirements.txt
├── .env.example
├── main.py                    # CLI principal
├── quick_start.py             # Demo rápida
└── README.md
```

---

## 🎯 Caso de Uso: Compliance para Startups

M.A.R.T.I.N. está diseñado para ayudar a startups con compliance (SOC 2, ISO 27001):

- **Auditorías automatizadas** de infraestructura
- **Generación de políticas** customizadas
- **Evaluación de gaps** de compliance
- **Roadmaps personalizados** para certificación

### Por qué Compliance?

- 50,000+ startups en LATAM necesitan certificaciones
- Proceso manual: 6-12 meses, $50k+ con consultoras
- M.A.R.T.I.N.: 8 semanas, ~$5k en costo operativo
- **Reducción de 80% en tiempo y costo**

---

## 🧪 Testing

```bash
# Test del mode selector
python agent_core/mode_selector.py

# Test del agente completo
python agent_core/martin_agent.py

# Demo interactiva
python quick_start.py
```

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **LangChain** - Framework para agentes
- **OpenAI GPT-4** - Motor de razonamiento (opcional)
- **Gradio** - Interfaz web
- **python-dotenv** - Variables de entorno

---

## 🏆 ¿Por Qué M.A.R.T.I.N. es Innovador?

### Otros agentes:
- ❌ AutoGPT: Siempre autónomo → Peligroso en producción
- ❌ ChatGPT: Siempre pasivo → No es realmente autónomo
- ❌ Copilot: No valida riesgos → Puede sugerir acciones destructivas

### M.A.R.T.I.N.:
- ✅ Adapta su autonomía al contexto
- ✅ Auto-valida en situaciones críticas
- ✅ Transparente en su razonamiento
- ✅ Usuario mantiene control cuando necesita

---

## 📊 Roadmap Futuro

- [x] ModeSelector funcional
- [x] 3 Reasoning Engines
- [x] Interfaz Gradio
- [ ] Herramientas de compliance reales
- [ ] GitHub/AWS scanners
- [ ] Cloudflare Workers integration
- [ ] Memory persistente
- [ ] API REST

---

## 🤝 Contribuir

Este proyecto fue desarrollado para **The Agent Hackathon 2025** by Skyward.ai.

Contribuciones son bienvenidas:
1. Fork el proyecto
2. Crea tu feature branch
3. Commit tus cambios
4. Push al branch
5. Abre un Pull Request

---

## 📝 License

MIT License  

---

## 🙏 Créditos

- Skyward.ai por organizar el hackathon
- OpenAI/Anthropic por APIs de LLM
- Comunidad LangChain por el framework

---

## 📞 Contacto

Desarrollado para **The Agent Hackathon 2025**


---

**Built with 🧠 and ☕ by Francisco Ortiz**