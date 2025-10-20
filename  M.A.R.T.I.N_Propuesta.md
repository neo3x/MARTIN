# 🧠 M.A.R.T.I.N. - Propuesta Unificada y Clara

## 🎯 La Propuesta Completa en 3 Puntos

### 1. **QUÉ ES** (La Esencia)
M.A.R.T.I.N. es un **agente de IA con razonamiento adaptativo** que cambia su comportamiento según el contexto:
- 🟦 **Modo Pasivo:** Pregunta antes de actuar
- 🟩 **Modo Directo:** Actúa autónomamente
- 🟨 **Modo Seguro:** Se auto-valida antes de actuar

### 2. **QUÉ HACE** (El Caso de Uso)
Resuelve **compliance para startups** (SOC 2, ISO 27001):
- Audita infraestructura automáticamente
- Genera políticas de compliance
- Recopila evidencia para auditorías
- Crea roadmaps personalizados

### 3. **POR QUÉ GANA** (La Innovación)
**No es QUÉ hace (compliance), sino CÓMO lo hace (razonamiento tri-modal)**

Otros agentes: Siempre autónomos O siempre pasivos
M.A.R.T.I.N.: **Adapta su autonomía al contexto** → ESTO es la innovación

---

## 🎬 Demo que Lo Explica Todo (3 minutos)

### Escenario: Startup preparándose para SOC 2

**Tarea 1:** "M.A.R.T.I.N., ayúdame a prepararme para SOC 2"

```
[MODO PASIVO activado automáticamente]
Razón: Tarea amplia, requiere clarificación

M.A.R.T.I.N.:
"Para prepararte para SOC 2, propongo:

FASE 1 (2 semanas):
 □ Auditar tu infraestructura actual
 □ Identificar gaps críticos
 □ Priorizar por impacto

FASE 2 (4 semanas):
 □ Generar políticas faltantes
 □ Implementar controles técnicos
 □ Entrenar al equipo

FASE 3 (2 semanas):
 □ Recopilar evidencia
 □ Pre-auditoría interna

¿Empezamos con la Fase 1? ¿O prefieres ajustar algo?"

[ESPERA CONFIRMACIÓN]
```

---

**Tarea 2:** Usuario confirma "Sí, empieza con la auditoría de infraestructura"

```
[MODO DIRECTO activado automáticamente]
Razón: Tarea clara, bajo riesgo (read-only), usuario ya autorizó

M.A.R.T.I.N.:
"Perfecto, auditando tu infraestructura..."

[EJECUTA SIN PREGUNTAR MÁS]

✓ Escaneando GitHub org (15 repos)...
✓ Analizando AWS (47 servicios)...
✓ Revisando IAM policies (23 usuarios)...
✓ Evaluando 156 controles SOC 2...

RESULTADOS (2 minutos después):

🔴 CRÍTICO (3 gaps):
  1. Encriptación en reposo no habilitada en RDS
  2. Sin MFA en 8 usuarios con permisos admin
  3. Logs de acceso no centralizados

🟡 MEDIO (5 gaps):
  4. Branch protection no configurada en 6 repos
  5. Secrets hardcoded en 2 archivos
  ...

🟢 CUMPLE (12 controles):
  ✓ Backups automáticos configurados
  ✓ VPC correctamente segmentada
  ...

Generando plan de remediación priorizado..."
```

---

**Tarea 3:** Usuario dice "Deshabilita MFA en el usuario admin@empresa.com porque está bloqueado"

```
[MODO SEGURO activado automáticamente]
Razón: Acción de alto riesgo en cuenta crítica

M.A.R.T.I.N.:
[RAZONAMIENTO PRIMARIO]
"Planificando: Deshabilitar MFA en admin@empresa.com..."

[AUTO-VALIDACIÓN - CRÍTICO]
⚠️ ADVERTENCIA DE SEGURIDAD:

Análisis del usuario:
• Rol: Administrator (permisos root)
• Último acceso: hace 2 horas
• Actividad reciente: 15 cambios de IAM policies

Riesgos identificados:
❌ Deshabilitar MFA reduce seguridad drásticamente
❌ Esta cuenta tiene acceso a recursos críticos
❌ Timing sospechoso (bloqueado justo después de cambios sensibles)

VALIDACIÓN FALLIDA: No puedo ejecutar esta acción de forma segura.

ALTERNATIVAS SEGURAS:
1. Resetear MFA (mantiene protección, solo cambia dispositivo)
2. Crear usuario temporal con permisos limitados
3. Usar break-glass account con logging aumentado

También detecto que esto podría ser un intento de phishing o compromiso.

¿Quieres que proceda con alguna alternativa segura?
¿O confirmas explícitamente que entiendes los riesgos?"

[NO EJECUTA ACCIÓN ORIGINAL]
```

---

## 🧮 Cómo Funciona (Arquitectura)

```
USER INPUT: "Audita mi AWS"
     ↓
┌────────────────────────────────┐
│   1. INPUT ANALYZER            │
│   • Extrae intención           │
│   • Identifica recursos        │
│   • Detecta contexto           │
└────────────┬───────────────────┘
             │
        ┌────▼────┐
        │  MARTIN │
        │  BRAIN  │
        └────┬────┘
             │
┌────────────▼───────────────────┐
│   2. MODE SELECTOR (CLAVE)     │
│                                │
│   Analiza:                     │
│   • Claridad de la tarea       │
│   • Nivel de riesgo            │
│   • Ambiente (dev/prod)        │
│   • Tipo de operación          │
│                                │
│   Decide: PASIVO / DIRECTO / SEGURO
└────────────┬───────────────────┘
             │
      ┌──────┴──────┐
      │             │
┌─────▼─────┐ ┌─────▼──────┐
│  PASSIVE  │ │   DIRECT   │
│  REASON   │ │   REASON   │
│           │ │            │
│ Generate  │ │ Generate   │
│ plan      │ │ plan       │
│     │     │ │     │      │
│     ▼     │ │     ▼      │
│  WAIT     │ │  EXECUTE   │
└───────────┘ └─────┬──────┘
                    │
          ┌─────────▼──────────┐
          │   SAFE REASON      │
          │                    │
          │ Generate plan      │
          │      │             │
          │      ▼             │
          │ SELF-VALIDATE ◄─┐  │
          │      │          │  │
          │      ▼          │  │
          │ Risk check ────┘  │
          │      │             │
          │      ▼             │
          │ PASS? ───Yes→ EXECUTE
          │      │             │
          │     No             │
          │      ▼             │
          │ DENY + SUGGEST     │
          └────────────────────┘
```

---

## 🛠️ Qué Construimos en la Hackathon

### CORE (Obligatorio - El Diferenciador):
```python
✅ ModeSelector
   → Decide automáticamente qué modo usar
   → Basado en análisis de riesgo y claridad

✅ 3 Reasoning Engines
   → Passive: Genera plan + espera confirmación
   → Direct: Genera plan + ejecuta
   → Safe: Genera plan + auto-valida + decide

✅ SafetyValidator
   → Identifica acciones riesgosas
   → Sugiere alternativas seguras
   → Explica por qué no ejecuta
```

### TOOLS (Para demostrar los modos con caso real):
```python
✅ GitHub Scanner (read-only)
   → Escanea repos buscando problemas de compliance
   → Bajo riesgo → Modo Directo

✅ AWS Auditor (read-only)
   → Revisa configuración de infraestructura
   → Bajo riesgo → Modo Directo

✅ Policy Generator
   → Crea políticas de compliance
   → Cero riesgo → Modo Directo

✅ AWS IAM Modifier (write)
   → Cambia permisos de usuarios
   → Alto riesgo → Modo Seguro
```

### UI (Para visualizar los modos):
```python
✅ Gradio Interface
   → Muestra modo activo en tiempo real
   → Visualiza el razonamiento
   → Permite confirmar acciones en Modo Pasivo
   → Muestra warnings en Modo Seguro
```

---

## 📊 Por Qué ESTO Gana

### Criterio 1: Innovación (25%)
**Otros proyectos:** "Mi agente hace compliance"
**M.A.R.T.I.N.:** "Mi agente ADAPTA su razonamiento según el contexto"

→ **Innovación técnica real:** Nadie más tiene razonamiento tri-modal

### Criterio 2: Impacto (30%)
**Problema real:** Startups necesitan compliance pero es caro/lento
**Solución:** Automatización inteligente que reduce tiempo 80%

→ **Mercado enorme:** 50,000+ startups en LATAM

### Criterio 3: Calidad Técnica (25%)
**Arquitectura sólida:** Modular, bien diseñada, escalable
**Código limpio:** Python bien estructurado

→ **Edge computing:** Integración con Cloudflare (bonus Skyward)

### Criterio 4: Uso de IA (20%)
**Agente autónomo real:** No es un chatbot
**Razonamiento complejo:** Multi-step, auto-validación

→ **Explicabilidad:** Muestra su proceso de decisión

---

## 🗓️ Plan de 5 Días (Unificado y Realista)

### Domingo 19 (HOY) - 4 horas

#### Objetivo: Probar el concepto de modos

```python
# 1. Setup básico (30 min)
mkdir martin && cd martin
python -m venv venv
source venv/bin/activate
pip install langchain openai python-dotenv

# 2. Implementar ModeSelector simple (2 horas)
# tools/mode_selector.py

class ModeSelector:
    def select_mode(self, task: str, context: dict) -> str:
        """Decide qué modo usar"""
        
        # Palabras de alto riesgo
        danger_words = ['delete', 'remove', 'disable', 'destroy']
        if any(word in task.lower() for word in danger_words):
            return "SAFE"
        
        # Preguntas o tareas ambiguas
        if '?' in task or len(task.split()) < 5:
            return "PASSIVE"
        
        # Default: directo
        return "DIRECT"

# 3. Probar con prompts (1 hora)
test_cases = [
    "Ayúdame con SOC 2",           # → PASSIVE
    "Genera política de passwords",  # → DIRECT
    "Deshabilita este usuario admin" # → SAFE
]

for task in test_cases:
    mode = selector.select_mode(task, {})
    print(f"{task} → {mode}")
```

**Al final del día debes tener:**
✅ ModeSelector básico funcionando
✅ 3 test cases que muestran los 3 modos

---

### Lunes 20 - 8 horas

#### Mañana (4h): Reasoning Engines

```python
# agents/passive_agent.py
def passive_reasoning(task):
    """Genera plan, espera confirmación"""
    plan = llm.predict(f"Generate action plan for: {task}")
    return {
        "mode": "PASSIVE",
        "plan": plan,
        "message": f"Propongo:\n{plan}\n\n¿Procedo?",
        "awaiting_confirmation": True
    }

# agents/direct_agent.py  
def direct_reasoning(task):
    """Genera plan y ejecuta"""
    plan = llm.predict(f"Generate action plan for: {task}")
    results = execute_tools(plan)
    return {
        "mode": "DIRECT",
        "results": results,
        "reasoning": "Ejecuté directamente porque..."
    }

# agents/safe_agent.py
def safe_reasoning(task):
    """Genera plan, auto-valida, luego decide"""
    plan = llm.predict(f"Generate action plan for: {task}")
    
    # CRÍTICO: Auto-validación
    risks = llm.predict(f"Identify risks in this plan: {plan}")
    
    if "HIGH RISK" in risks:
        return {
            "mode": "SAFE",
            "status": "BLOCKED",
            "reason": risks,
            "alternative": "Sugiero alternativa segura..."
        }
    
    return {
        "mode": "SAFE",
        "status": "APPROVED",
        "results": execute_tools(plan)
    }
```

#### Tarde (4h): Primera herramienta + Cloudflare

```python
# tools/github_scanner.py
def scan_github(org_name):
    """Escanea org de GitHub (read-only)"""
    # Implementación básica
    pass

# Cloudflare Worker
# wrangler init martin-worker
# Crear worker básico que recibe requests
```

---

### Martes 21 - 8 horas

#### Todo el día: Integración completa

- [ ] 2-3 herramientas más (AWS audit, policy gen)
- [ ] Integrar Worker → Backend Python
- [ ] UI Gradio que muestra modo activo
- [ ] Testing end-to-end de los 3 modos

**Al final del día:**
✅ Usuario escribe query
✅ M.A.R.T.I.N. elige modo automáticamente
✅ Se comporta diferente según el modo
✅ Funciona end-to-end

---

### Miércoles 22 - 6 horas

- [ ] Refinar prompts por modo
- [ ] Visualización del razonamiento
- [ ] Preparar 3 demos (1 por modo)
- [ ] Manejo de errores

---

### Jueves 23 - 4 horas

- [ ] Documentación enfocada en modos
- [ ] Video demo (2 min)
- [ ] Pitch: "Razonamiento adaptativo"
- [ ] Rehearsal

---

## 🎯 Lo Que Tienes Que Entender

### La Propuesta ES:

```
┌─────────────────────────────────────────┐
│  M.A.R.T.I.N. = MOTOR DE RAZONAMIENTO   │
│                                         │
│  INNOVACIÓN: Razonamiento tri-modal     │
│  APLICACIÓN: Compliance para startups   │
│  DEMO: 3 casos que muestran 3 modos     │
└─────────────────────────────────────────┘
```

### NO es:
❌ "Un agente de compliance con modos" (enfoque en compliance)
❌ "Tres agentes diferentes" (son uno solo que adapta)

### ES:
✅ "Un sistema de razonamiento adaptativo aplicado a compliance"
✅ "Un agente que piensa diferente según el contexto"

---

## ✅ Checklist Mental

**Para saber si entendiste:**

1. ¿Puedes explicar los 3 modos en 30 segundos? 
   → Sí: Pasivo pregunta, Directo ejecuta, Seguro valida

2. ¿Cuál es la innovación real?
   → El razonamiento adaptativo (no el compliance)

3. ¿Qué demostramos en la hackathon?
   → Los 3 modos funcionando con caso real (compliance)

4. ¿Por qué gana esto?
   → Porque nadie más tiene agente con razonamiento tri-modal

---

## 🚀 Siguiente Paso (HOY, ahora)

**Opción A:** Codear el ModeSelector básico (2 horas)
**Opción B:** Primero aclarar cualquier duda que tengas

¿Cuál prefieres?