# 🧠 M.A.R.T.I.N.

### Modular Assistant for Reasoning, Tactics, Inference and Navigation

**M.A.R.T.I.N.** es un agente autónomo de inteligencia artificial diseñado para operar como un sistema modular capaz de razonar, planificar y ejecutar tareas de forma independiente. Su arquitectura está enfocada en adaptarse a distintos entornos y niveles de complejidad, desde tareas técnicas hasta escenarios de toma de decisiones asistida.

Este repositorio contiene la documentación, arquitectura y código base del agente, desarrollado originalmente para **The Agent Hackathon 2025** organizado por Skyward.ai y CommunityOS.io.

---

## 📌 ¿Qué es M.A.R.T.I.N.?

**M.A.R.T.I.N.** significa:

> **Modular Assistant for Reasoning, Tactics, Inference and Navigation**

Es un **agente de IA modular y autónomo**, cuya principal función es recibir instrucciones de alto nivel y ejecutar procesos que requieren análisis, lógica, planificación y uso de herramientas externas. A diferencia de un chatbot tradicional, M.A.R.T.I.N. opera como un sistema cognitivo que descompone tareas, evalúa rutas posibles y actúa deliberadamente.

---

## ⚙️ Características

* **Razonamiento paso a paso**: descompone problemas complejos y actúa en secuencia lógica.
* **Módulos independientes**: cada componente (razonador, planificador, ejecutor, memoria) funciona de forma desacoplada.
* **Memoria persistente**: puede recordar decisiones, datos e interacciones para mejorar su desempeño.
* **Multi-entorno**: diseñado para funcionar localmente (offline) o en la nube, en infraestructura como HuggingFace, Colab, o Cloudflare Workers.
* **Extensible**: puede incorporar nuevas herramientas, habilidades o datos sin alterar la arquitectura base.
* **Modo Seguro**: puede validar su lógica antes de ejecutar decisiones sensibles.

---

## 🎛️ Modos de Operación

M.A.R.T.I.N. puede trabajar bajo tres modos distintos según el contexto y el nivel de autonomía deseado:

1. **Modo Pasivo**

   * Solo responde a instrucciones sin tomar decisiones autónomas.
   * Ideal para entornos donde se desea control total por parte del usuario.

2. **Modo Directo**

   * M.A.R.T.I.N. razona, planifica y ejecuta tareas de forma autónoma.
   * Útil para tareas automáticas repetitivas o análisis independientes.

3. **Modo Seguro**

   * El agente evalúa críticamente su propio razonamiento antes de ejecutar acciones.
   * Puede solicitar confirmación del usuario o pasar por una lógica de revisión.
   * Ideal para entornos críticos como ciberseguridad, legal o sistemas sensibles.

---

## 🧩 Arquitectura Modular

```txt
[ Usuario ]
     ↓
[ Interfaz (CLI / Gradio / API REST) ]
     ↓
[ Núcleo LLM (local u online) ]
     ↓
[ Módulos: ]
  - Reasoning Core (descompone, evalúa)
  - Planner (define tareas y prioridades)
  - Memory (corto y largo plazo)
  - Toolset (uso de herramientas externas)
  - Navigator (gestiona flujos y decisiones)
```

---

## 🎯 ¿Para qué sirve?

M.A.R.T.I.N. puede ser adaptado para múltiples casos de uso donde la toma de decisiones basada en información, el razonamiento lógico o la ejecución automatizada de tareas complejas es clave. Algunos ejemplos:

* **Ciberseguridad**: análisis de vulnerabilidades y sugerencia de medidas correctivas.
* **Educación personalizada**: creación de planes de estudio adaptativos según necesidades del estudiante.
* **Soporte técnico inteligente**: diagnóstico de problemas técnicos y guía paso a paso.
* **Análisis documental**: revisión de contratos, normativas o PDFs técnicos para extraer conclusiones accionables.

---

## 🚀 Estado actual

Este repositorio contiene:

* [x] Estructura modular base en Python
* [x] Agente funcional con integración LLM local u OpenAI
* [x] Interfaz vía CLI / Gradio
* [x] Planificador simple y herramientas externas
* [x] Demo funcional para tareas específicas

---

## 📂 Estructura del repositorio

```
├── /agent_core/        # Núcleo lógico del agente (razonamiento, planificación)
├── /tools/             # Módulos integrables externos (buscadores, APIs, parseadores)
├── /memory/            # Adaptadores de memoria y almacenamiento de contexto
├── /interface/         # Gradio / CLI o endpoints REST
├── /configs/           # Parámetros y prompts del agente
├── /docs/              # Diagramas, documentación y casos de uso
└── main.py             # Script principal de ejecución
```

---

## 📄 Licencia

Este proyecto se distribuye bajo licencia MIT. Puedes modificar, redistribuir y adaptar según tus necesidades.

---

> Si estás participando en The Agent Hackathon, te invitamos a explorar este agente, clonarlo, adaptarlo y expandirlo. Que M.A.R.T.I.N. te sirva como base para construir el tuyo.

---

🧪 *Construido por Francisco y equipo para explorar nuevas formas de razonamiento autónomo aplicado.*
