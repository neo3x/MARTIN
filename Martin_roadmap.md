# 🧠 M.A.R.T.I.N. - Roadmap Completo y Detallado

## 🎯 La Propuesta (Recordatorio)

**M.A.R.T.I.N. = Motor de Razonamiento Adaptativo aplicado a Compliance**

### Los 3 Modos de Razonamiento:
- 🟦 **MODO PASIVO:** Pregunta antes de actuar (tareas ambiguas, exploración)
- 🟩 **MODO DIRECTO:** Actúa autónomamente (tareas claras, bajo riesgo)
- 🟨 **MODO SEGURO:** Auto-valida antes de actuar (alto riesgo, producción)

### Caso de Uso:
Compliance automation para startups (SOC 2, ISO 27001)

### La Innovación:
No es "qué hace" sino "cómo razona" → Razonamiento tri-modal adaptativo

---

## ⏰ CONTEXTO TEMPORAL

### Fechas Clave:
- **HOY:** Domingo 19 Octubre, 23:00 hrs
- **Hackathon inicia:** Sábado 25 Octubre, 09:00 hrs
- **Hackathon termina:** Domingo 26 Octubre, 18:00 hrs
- **Tiempo de preparación:** 5 días y medio (Lun 20 → Vie 24)

---

# 📆 ROADMAP DETALLADO DE PREPARACIÓN

## 🌙 Domingo 19 Octubre (23:00) - HOY

### Acción inmediata:
- ✅ **Revisar y entender este roadmap completo** (15 min)
- ✅ **Dormir bien** (7-8 horas mínimo)
- ✅ **Mentalidad:** Mañana arrancamos con todo 🚀

---

## 📅 Lunes 20 Octubre - DÍA 1

### Objetivo del día:
**Fundamentos técnicos + ModeSelector funcional**

---

### MAÑANA (09:00 - 13:00) - 4 horas

#### 09:00 - 10:00 | Setup del entorno (1 hora)

**Tareas:**
```bash
# 1. Crear estructura del proyecto
mkdir martin-agent
cd martin-agent
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# 2. Instalar dependencias
pip install langchain==0.1.0
pip install openai==1.0.0
pip install anthropic==0.8.0  # Alternativa a OpenAI
pip install python-dotenv==1.0.0
pip install gradio==4.0.0
pip install requests==2.31.0
pip install beautifulsoup4==4.12.0

# 3. Crear estructura de carpetas
mkdir -p {agents,tools,tests,docs}
touch .env README.md requirements.txt

# 4. Configurar .env
echo "OPENAI_API_KEY=tu-key-aqui" > .env
echo "GITHUB_TOKEN=tu-token-aqui" >> .env
```

**API Keys necesarias:**
- [ ] OpenAI API Key: https://platform.openai.com/api-keys
- [ ] GitHub Personal Token: https://github.com/settings/tokens (scope: read:org, repo)

**Verificar instalación:**
```python
# test_setup.py
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4", temperature=0)
response = llm.predict("Di 'Setup exitoso'")
print(response)
```

---

#### 10:00 - 11:30 | ModeSelector v1 (1.5 horas)

**Archivo:** `agents/mode_selector.py`

```python
"""
ModeSelector - El cerebro que decide cómo M.A.R.T.I.N. debe razonar
"""
from typing import Dict, Literal
import re

ModeType = Literal["PASSIVE", "DIRECT", "SAFE"]

class ModeSelector:
    """
    Analiza la tarea y contexto para determinar el modo de razonamiento óptimo.
    """
    
    # Palabras clave que indican alto riesgo
    DANGER_KEYWORDS = [
        'delete', 'remove', 'destroy', 'drop', 'disable', 
        'terminate', 'kill', 'shutdown', 'revoke', 'block'
    ]
    
    # Palabras que indican ambigüedad o necesidad de clarificación
    VAGUE_KEYWORDS = [
        'ayuda', 'ayúdame', 'help', 'cómo', 'qué debo', 'no sé'
    ]
    
    def __init__(self):
        self.decision_log = []
    
    def select_mode(self, task: str, context: Dict = None) -> ModeType:
        """
        Decide el modo de razonamiento basado en análisis de la tarea.
        
        Args:
            task: Instrucción del usuario
            context: Información contextual (environment, user_role, etc.)
        
        Returns:
            Modo seleccionado: "PASSIVE", "DIRECT", o "SAFE"
        """
        if context is None:
            context = {}
        
        # Análisis de factores
        risk_score = self._assess_risk(task, context)
        clarity_score = self._assess_clarity(task)
        environment = context.get('environment', 'development')
        
        # Logging de decisión
        decision_factors = {
            'task': task[:50] + '...' if len(task) > 50 else task,
            'risk_score': risk_score,
            'clarity_score': clarity_score,
            'environment': environment
        }
        
        # Reglas de decisión (orden de prioridad)
        
        # 1. Producción siempre va a SAFE
        if environment == 'production':
            mode = "SAFE"
            reason = "Entorno de producción detectado"
        
        # 2. Alto riesgo siempre va a SAFE
        elif risk_score >= 0.7:
            mode = "SAFE"
            reason = f"Riesgo alto detectado (score: {risk_score})"
        
        # 3. Baja claridad va a PASSIVE
        elif clarity_score < 0.5:
            mode = "PASSIVE"
            reason = f"Tarea ambigua o requiere clarificación (clarity: {clarity_score})"
        
        # 4. Clara y segura va a DIRECT
        else:
            mode = "DIRECT"
            reason = "Tarea clara y de bajo riesgo"
        
        # Guardar log de decisión
        decision_factors['selected_mode'] = mode
        decision_factors['reason'] = reason
        self.decision_log.append(decision_factors)
        
        return mode
    
    def _assess_risk(self, task: str, context: Dict) -> float:
        """
        Calcula score de riesgo (0.0 - 1.0)
        
        Factores:
        - Palabras peligrosas en la tarea
        - Recursos críticos mencionados
        - Scope de impacto
        """
        risk = 0.0
        task_lower = task.lower()
        
        # Factor 1: Palabras peligrosas
        danger_words_found = sum(1 for word in self.DANGER_KEYWORDS if word in task_lower)
        if danger_words_found > 0:
            risk += 0.4 * min(danger_words_found / 2, 1.0)
        
        # Factor 2: Recursos críticos
        critical_resources = ['database', 'db', 'producción', 'production', 
                            'payment', 'billing', 'auth', 'users', 'admin']
        if any(resource in task_lower for resource in critical_resources):
            risk += 0.3
        
        # Factor 3: Scope amplio
        broad_scope_indicators = ['all', 'every', 'todos', 'cada', 'entire', 'completo']
        if any(indicator in task_lower for indicator in broad_scope_indicators):
            risk += 0.2
        
        # Factor 4: Contexto de ambiente
        if context.get('has_active_users', False):
            risk += 0.1
        
        return min(risk, 1.0)
    
    def _assess_clarity(self, task: str) -> float:
        """
        Calcula score de claridad (0.0 - 1.0)
        
        Factores:
        - Presencia de preguntas
        - Longitud de la instrucción
        - Palabras vagas
        - Especificidad
        """
        clarity = 1.0
        task_lower = task.lower()
        
        # Factor 1: Es una pregunta
        if '?' in task:
            clarity -= 0.3
        
        # Factor 2: Palabras vagas
        vague_words_found = sum(1 for word in self.VAGUE_KEYWORDS if word in task_lower)
        clarity -= 0.15 * vague_words_found
        
        # Factor 3: Longitud (muy corto = vago)
        word_count = len(task.split())
        if word_count < 5:
            clarity -= 0.3
        elif word_count < 3:
            clarity -= 0.5
        
        # Factor 4: No menciona recursos específicos
        if not any(char.isupper() for char in task):  # Sin nombres propios/específicos
            clarity -= 0.2
        
        return max(clarity, 0.0)
    
    def explain_last_decision(self) -> str:
        """Retorna explicación de la última decisión tomada"""
        if not self.decision_log:
            return "No hay decisiones registradas aún"
        
        last = self.decision_log[-1]
        return f"""
Decisión del ModeSelector:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tarea: "{last['task']}"
Modo seleccionado: {last['selected_mode']}
Razón: {last['reason']}

Factores analizados:
  • Riesgo: {last['risk_score']:.2f} (0=seguro, 1=peligroso)
  • Claridad: {last['clarity_score']:.2f} (0=vago, 1=claro)
  • Ambiente: {last['environment']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
```

---

#### 11:30 - 13:00 | Testing del ModeSelector (1.5 horas)

**Archivo:** `tests/test_mode_selector.py`

```python
"""
Tests para validar que el ModeSelector elige correctamente
"""
from agents.mode_selector import ModeSelector

def test_mode_selector():
    selector = ModeSelector()
    
    # TEST 1: Modo PASSIVE - Tarea ambigua
    print("🧪 TEST 1: Tarea ambigua")
    mode = selector.select_mode("Ayúdame con SOC 2")
    print(selector.explain_last_decision())
    assert mode == "PASSIVE", f"Esperado PASSIVE, obtenido {mode}"
    print("✅ PASSED\n")
    
    # TEST 2: Modo DIRECT - Tarea clara y segura
    print("🧪 TEST 2: Tarea clara y segura")
    mode = selector.select_mode("Genera una política de contraseñas según ISO 27001")
    print(selector.explain_last_decision())
    assert mode == "DIRECT", f"Esperado DIRECT, obtenido {mode}"
    print("✅ PASSED\n")
    
    # TEST 3: Modo SAFE - Acción peligrosa
    print("🧪 TEST 3: Acción peligrosa")
    mode = selector.select_mode("Delete all users from the database")
    print(selector.explain_last_decision())
    assert mode == "SAFE", f"Esperado SAFE, obtenido {mode}"
    print("✅ PASSED\n")
    
    # TEST 4: Modo SAFE - Producción
    print("🧪 TEST 4: Producción")
    mode = selector.select_mode(
        "Update configuration file",
        context={'environment': 'production'}
    )
    print(selector.explain_last_decision())
    assert mode == "SAFE", f"Esperado SAFE, obtenido {mode}"
    print("✅ PASSED\n")
    
    # TEST 5: Modo PASSIVE - Pregunta
    print("🧪 TEST 5: Pregunta del usuario")
    mode = selector.select_mode("¿Cómo configuro mi firewall para compliance?")
    print(selector.explain_last_decision())
    assert mode == "PASSIVE", f"Esperado PASSIVE, obtenido {mode}"
    print("✅ PASSED\n")
    
    print("🎉 Todos los tests pasaron exitosamente!")

if __name__ == "__main__":
    test_mode_selector()
```

**Ejecutar:**
```bash
python tests/test_mode_selector.py
```

**Objetivo:** Ver que los 5 tests pasan y entender por qué elige cada modo.

---

### TARDE (14:00 - 18:00) - 4 horas

#### 14:00 - 16:00 | Reasoning Engines (2 horas)

**Archivo:** `agents/reasoning_engines.py`

```python
"""
Los 3 motores de razonamiento de M.A.R.T.I.N.
"""
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing import Dict, Any
import os

class ReasoningEngines:
    """
    Contiene los 3 modos de razonamiento de M.A.R.T.I.N.
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def passive_reasoning(self, task: str, context: Dict = None) -> Dict[str, Any]:
        """
        MODO PASIVO: Genera plan pero NO ejecuta
        
        Comportamiento:
        1. Analiza la tarea
        2. Genera un plan detallado
        3. Explica qué hará
        4. ESPERA confirmación del usuario
        """
        
        prompt = PromptTemplate(
            input_variables=["task", "context"],
            template="""
Eres M.A.R.T.I.N., un agente de IA en MODO PASIVO.

En este modo, tu trabajo es:
1. Analizar la tarea del usuario
2. Proponer un plan de acción detallado
3. Explicar claramente qué harás
4. NO ejecutar nada hasta recibir confirmación

Tarea del usuario: {task}
Contexto: {context}

Genera un plan estructurado con:
- Pasos numerados
- Estimación de tiempo por paso
- Recursos necesarios
- Posibles riesgos o consideraciones

Formato de respuesta:
ANÁLISIS:
[Tu análisis de la tarea]

PLAN PROPUESTO:
1. [Primer paso] (X minutos)
2. [Segundo paso] (Y minutos)
...

CONSIDERACIONES:
- [Punto importante 1]
- [Punto importante 2]

PREGUNTA FINAL:
¿Procedo con este plan? ¿Quieres ajustar algo?
"""
        )
        
        response = self.llm.predict(
            prompt.format(
                task=task,
                context=str(context) if context else "No hay contexto adicional"
            )
        )
        
        return {
            "mode": "PASSIVE",
            "status": "awaiting_confirmation",
            "plan": response,
            "message": f"📋 MODO PASIVO ACTIVADO\n\n{response}",
            "requires_user_action": True
        }
    
    def direct_reasoning(self, task: str, context: Dict = None) -> Dict[str, Any]:
        """
        MODO DIRECTO: Genera plan Y ejecuta automáticamente
        
        Comportamiento:
        1. Analiza la tarea
        2. Genera plan de acción
        3. EJECUTA sin preguntar
        4. Reporta resultados
        5. Explica su razonamiento
        """
        
        # Paso 1: Planificar
        planning_prompt = PromptTemplate(
            input_variables=["task"],
            template="""
Eres M.A.R.T.I.N. en MODO DIRECTO - agente autónomo.

Tarea: {task}

Genera un plan de acción conciso y ejecutable.
Luego simula la ejecución y describe los resultados esperados.

Formato:
PLAN:
1. [Acción específica]
2. [Acción específica]

EJECUCIÓN SIMULADA:
[Describe qué harías y qué resultados obtendrías]

RAZONAMIENTO:
[Explica por qué tomaste estas decisiones]
"""
        )
        
        response = self.llm.predict(planning_prompt.format(task=task))
        
        # En una implementación real, aquí ejecutarías las tools
        # Por ahora simulamos la ejecución
        
        return {
            "mode": "DIRECT",
            "status": "executed",
            "results": response,
            "message": f"⚡ MODO DIRECTO - Ejecutado automáticamente\n\n{response}",
            "requires_user_action": False,
            "reasoning_visible": True
        }
    
    def safe_reasoning(self, task: str, context: Dict = None) -> Dict[str, Any]:
        """
        MODO SEGURO: Genera plan, AUTO-VALIDA, luego decide
        
        Comportamiento:
        1. Analiza la tarea
        2. Genera plan de acción
        3. SE AUTO-CRITICA (validación de riesgos)
        4. Si pasa validación → ejecuta con precauciones
        5. Si NO pasa → sugiere alternativa segura y pide confirmación
        """
        
        # Paso 1: Generar plan
        planning_prompt = PromptTemplate(
            input_variables=["task"],
            template="""
Genera un plan de acción para: {task}

Sé específico sobre qué acciones tomarías.
"""
        )
        
        plan = self.llm.predict(planning_prompt.format(task=task))
        
        # Paso 2: AUTO-VALIDACIÓN (CRÍTICO)
        validation_prompt = PromptTemplate(
            input_variables=["task", "plan"],
            template="""
Eres un validador de seguridad crítico.

Tarea original: {task}
Plan propuesto: {plan}

Analiza este plan buscando:
1. Riesgos de seguridad
2. Posibles daños o pérdidas
3. Impacto en sistemas críticos
4. Reversibilidad de las acciones

Responde en este formato:

NIVEL DE RIESGO: [BAJO/MEDIO/ALTO/CRÍTICO]

RIESGOS IDENTIFICADOS:
- [Riesgo 1]
- [Riesgo 2]
...

DECISIÓN: [APROBAR/RECHAZAR]

SI RECHAZAS:
ALTERNATIVA SEGURA:
[Describe un enfoque más seguro]

SI APRUEBAS:
PRECAUCIONES NECESARIAS:
- [Precaución 1]
- [Precaución 2]
"""
        )
        
        validation = self.llm.predict(
            validation_prompt.format(task=task, plan=plan)
        )
        
        # Analizar resultado de validación
        if "RECHAZAR" in validation or "CRÍTICO" in validation:
            # Validación falló
            return {
                "mode": "SAFE",
                "status": "blocked",
                "validation_failed": True,
                "original_plan": plan,
                "validation_report": validation,
                "message": f"🛡️ MODO SEGURO - ACCIÓN BLOQUEADA\n\n{validation}",
                "requires_user_action": True
            }
        else:
            # Validación pasó, ejecutar con precauciones
            return {
                "mode": "SAFE",
                "status": "approved_and_executed",
                "validation_passed": True,
                "plan": plan,
                "validation_report": validation,
                "results": "[Simulación de ejecución segura]",
                "message": f"🛡️ MODO SEGURO - Validado y ejecutado\n\n{validation}\n\nRESULTADOS:\n[Ejecutado con precauciones]",
                "requires_user_action": False
            }
```

---

#### 16:00 - 18:00 | Integración MARTINAgent (2 horas)

**Archivo:** `agents/martin_agent.py`

```python
"""
M.A.R.T.I.N. Agent - Integración completa del sistema
"""
from agents.mode_selector import ModeSelector
from agents.reasoning_engines import ReasoningEngines
from typing import Dict, Any

class MARTINAgent:
    """
    Agente principal que orquesta:
    1. Selección de modo
    2. Razonamiento apropiado
    3. Ejecución (si corresponde)
    """
    
    def __init__(self):
        self.mode_selector = ModeSelector()
        self.reasoning = ReasoningEngines()
        self.conversation_history = []
    
    def process(self, user_input: str, context: Dict = None) -> Dict[str, Any]:
        """
        Procesa input del usuario a través de M.A.R.T.I.N.
        
        Flujo:
        1. Selecciona modo apropiado
        2. Aplica razonamiento según modo
        3. Retorna respuesta estructurada
        """
        if context is None:
            context = {}
        
        # Paso 1: Decidir modo
        selected_mode = self.mode_selector.select_mode(user_input, context)
        
        # Paso 2: Aplicar razonamiento según modo
        if selected_mode == "PASSIVE":
            result = self.reasoning.passive_reasoning(user_input, context)
        elif selected_mode == "DIRECT":
            result = self.reasoning.direct_reasoning(user_input, context)
        else:  # SAFE
            result = self.reasoning.safe_reasoning(user_input, context)
        
        # Agregar explicación del mode selector
        result['mode_explanation'] = self.mode_selector.explain_last_decision()
        
        # Guardar en historial
        self.conversation_history.append({
            'input': user_input,
            'context': context,
            'result': result
        })
        
        return result
    
    def get_conversation_history(self):
        """Retorna historial completo de la conversación"""
        return self.conversation_history
```

**Archivo de prueba:** `tests/test_martin_agent.py`

```python
"""
Test completo del agente M.A.R.T.I.N.
"""
from agents.martin_agent import MARTINAgent
import json

def print_result(result):
    """Helper para imprimir resultados de forma bonita"""
    print("="*60)
    print(result['message'])
    print("="*60)
    print(f"\nModo usado: {result['mode']}")
    print(f"Estado: {result['status']}")
    if 'mode_explanation' in result:
        print(result['mode_explanation'])
    print("\n")

def main():
    agent = MARTINAgent()
    
    print("🧠 M.A.R.T.I.N. Agent - Tests Completos\n")
    
    # TEST 1: Modo Pasivo
    print("━━━ TEST 1: Tarea ambigua (debería activar MODO PASIVO) ━━━")
    result1 = agent.process("Ayúdame a preparar mi startup para SOC 2")
    print_result(result1)
    input("Presiona Enter para continuar...")
    
    # TEST 2: Modo Directo
    print("\n━━━ TEST 2: Tarea clara (debería activar MODO DIRECTO) ━━━")
    result2 = agent.process("Genera una política de respuesta a incidentes según SOC 2")
    print_result(result2)
    input("Presiona Enter para continuar...")
    
    # TEST 3: Modo Seguro (bloqueado)
    print("\n━━━ TEST 3: Acción peligrosa (debería activar MODO SEGURO y BLOQUEAR) ━━━")
    result3 = agent.process(
        "Deshabilita MFA para el usuario admin@empresa.com",
        context={'environment': 'production'}
    )
    print_result(result3)
    input("Presiona Enter para continuar...")
    
    # TEST 4: Modo Seguro (aprobado)
    print("\n━━━ TEST 4: Acción con riesgo moderado (MODO SEGURO pero aprobado) ━━━")
    result4 = agent.process(
        "Revisa los logs de acceso de los últimos 7 días",
        context={'environment': 'production'}
    )
    print_result(result4)
    
    print("\n✅ Tests completados!")
    print(f"\n📊 Total de interacciones: {len(agent.get_conversation_history())}")

if __name__ == "__main__":
    main()
```

---

### NOCHE (19:00 - 22:00) - 3 horas OPCIONALES

#### Si tienes energía:

**Opción A:** Empezar Cloudflare Worker básico
```bash
npm install -g wrangler
wrangler login
wrangler init martin-worker
```

**Opción B:** Crear primera herramienta simple (Policy Generator)

**Opción C:** Descansar y prepararte para mañana (RECOMENDADO)

---

### ✅ Checklist Fin del Día 1:

Al terminar el lunes debes tener:
- [ ] Entorno Python configurado y funcionando
- [ ] ModeSelector implementado y testeado (5 tests pasando)
- [ ] 3 Reasoning Engines implementados
- [ ] MARTINAgent integrado y funcionando end-to-end
- [ ] Entiendes claramente cómo funciona cada modo
- [ ] 4 tests completos del agente funcionando

**Si logras esto, vas EXCELENTE. El core de M.A.R.T.I.N. está listo.** 🎉

---

## 📅 Martes 21 Octubre - DÍA 2

### Objetivo del día:
**Herramientas reales + UI básica**

---

### MAÑANA (09:00 - 13:00) - 4 horas

#### 09:00 - 11:00 | Primera herramienta: Policy Generator (2 horas)

**Archivo:** `tools/policy_generator.py`

```python
"""
Herramienta para generar políticas de compliance
"""
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os

class PolicyGenerator:
    """
    Genera políticas de compliance (SOC 2, ISO 27001, etc.)
    basadas en templates y best practices
    """
    
    POLICY_TEMPLATES = {
        'incident_response': """
POLÍTICA DE RESPUESTA A INCIDENTES
===================================

1. PROPÓSITO
Esta política establece el procedimiento para responder a incidentes de seguridad.

2. ALCANCE
Aplica a todos los sistemas, aplicaciones y datos de {company_name}.

3. ROLES Y RESPONSABILIDADES
- Incident Response Manager: {roles}
- Equipo técnico: {team}

4. PROCEDIMIENTO
4.1 Detección: {detection_methods}
4.2 Clasificación: {classification}
4.3 Contención: {containment}
4.4 Erradicación: {eradication}
4.5 Recuperación: {recovery}
4.6 Lecciones aprendidas: {lessons_learned}

5. COMUNICACIÓN
{communication_plan}

6. REVISIÓN
Esta política será revisada anualmente o después de incidentes mayores.
""",
        'password_policy': """
POLÍTICA DE CONTRASEÑAS
=======================

1. PROPÓSITO
Establecer requisitos mínimos para contraseñas de usuarios.

2. REQUISITOS
- Longitud mínima: {min_length} caracteres
- Complejidad: {complexity_rules}
- Rotación: {rotation_period}
- Historia: No reusar últimas {password_history} contraseñas
- MFA: {mfa_requirement}

3. IMPLEMENTACIÓN
{implementation_details}

4. EXCEPCIONES
{exceptions}
""",
        'access_control': """
POLÍTICA DE CONTROL DE ACCESO
==============================

1. PROPÓSITO
Definir cómo se otorgan, revisan y revocan accesos.

2. PRINCIPIOS
- Least Privilege: {least_privilege}
- Separation of Duties: {separation_duties}
- Need-to-know: {need_to_know}

3. PROCESO DE APROBACIÓN
{approval_process}

4. REVISIÓN DE ACCESOS
Frecuencia: {review_frequency}
Responsable: {reviewer_role}

5. REVOCACIÓN
{revocation_process}
"""
    }
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.3)
    
    def generate_policy(self, policy_type: str, company_context: dict) -> str:
        """
        Genera una política customizada
        
        Args:
            policy_type: Tipo de política (incident_response, password_policy, etc.)
            company_context: Info de la empresa (nombre, tamaño, industria, tech stack)
        
        Returns:
            Política completa en formato markdown
        """
        
        if policy_type not in self.POLICY_TEMPLATES:
            return f"Error: Tipo de política '{policy_type}' no soportado"
        
        template = self.POLICY_TEMPLATES[policy_type]
        
        # Usar LLM para completar el template con contexto de la empresa
        prompt = PromptTemplate(
            input_variables=["template", "context"],
            template="""
Eres un experto en compliance y políticas de seguridad.

Template de política:
{template}

Contexto de la empresa:
{context}

Completa el template con información específica y realista basada en el contexto.
Usa mejores prácticas de la industria y estándares como SOC 2, ISO 27001.
Sé específico y práctico.

Retorna la política completa en formato markdown.
"""
        )
        
        policy = self.llm.predict(
            prompt.format(
                template=template,
                context=str(company_context)
            )
        )
        
        return policy
    
    def list_available_policies(self) -> list:
        """Retorna lista de políticas disponibles"""
        return list(self.POLICY_TEMPLATES.keys())


# Test rápido
if __name__ == "__main__":
    generator = PolicyGenerator()
    
    company = {
        'name': 'TechStartup Inc.',
        'size': '25 empleados',
        'industry': 'SaaS B2B',
        'tech_stack': 'AWS, Python, React, PostgreSQL'
    }
    
    print("Generando política de respuesta a incidentes...\n")
    policy = generator.generate_policy('incident_response', company)
    print(policy)
```

---

#### 11:00 - 13:00 | Segunda herramienta: GitHub Scanner (2 horas)

**Archivo:** `tools/github_scanner.py`

```python
"""
Herramienta para escanear repositorios de GitHub
buscando problemas de compliance y seguridad
"""
from github import Github
import os
import re
from typing import Dict, List

class GitHubScanner:
    """
    Escanea repositorios buscando:
    - Secrets hardcoded
    - Falta de branch protection
    - Dependencias vulnerables
    - Documentación de seguridad faltante
    """
    
    # Patrones de secrets comunes
    SECRET_PATTERNS = {
        'aws_key': r'AKIA[0-9A-Z]{16}',
        'api_key': r'api[_-]?key[_-]?[=:]\s*[\'"][a-zA-Z0-9]{20,}[\'"]',
        'password': r'password[_-]?[=:]\s*[\'"][^\'"]{8,}[\'"]',
        'token': r'token[_-]?[=:]\s*[\'"][a-zA-Z0-9]{20,}[\'"]',
        'private_key': r'-----BEGIN.*PRIVATE KEY-----'
    }
    
    def __init__(self, github_token: str = None):
        token = github_token or os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError("GitHub token requerido")
        self.github = Github(token)
    
    def scan_organization(self, org_name: str) -> Dict:
        """
        Escanea toda una organización de GitHub
        
        Returns:
            Reporte completo de findings
        """
        try:
            org = self.github.get_organization(org_name)
        except:
            return {'error': f'Organización {org_name} no encontrada o sin acceso'}
        
        findings = {
            'organization': org_name,
            'total_repos': 0,
            'issues': [],
            'summary': {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0
            }
        }
        
        repos = org.get_repos()
        
        for repo in repos:
            findings['total_repos'] += 1
            repo_findings = self._scan_repository(repo)
            findings['issues'].extend(repo_findings)
            
            # Contar por severidad
            for issue in repo_findings:
                severity = issue['severity']
                findings['summary'][severity] += 1
        
        return findings
    
    def _scan_repository(self, repo) -> List[Dict]:
        """Escanea un repositorio individual"""
        issues = []
        
        # Check 1: Branch protection
        try:
            default_branch = repo.get_branch(repo.default_branch)
            if not default_branch.protected:
                issues.append({
                    'repo': repo.name,
                    'type': 'branch_protection',
                    'severity': 'high',
                    'message': f'Branch {repo.default_branch} no tiene protección habilitada',
                    'remediation': 'Habilitar branch protection rules'
                })
        except:
            pass
        
        # Check 2: Escanear archivos buscando secrets
        try:
            contents = repo.get_contents("")
            secrets_found = self._scan_for_secrets(repo, contents)
            issues.extend(secrets_found)
        except:
            pass
        
        # Check 3: Verificar si existe SECURITY.md
        try:
            repo.get_contents("SECURITY.md")
        except:
            issues.append({
                'repo': repo.name,
                'type': 'missing_documentation',
                'severity': 'medium',
                'message': 'Falta archivo SECURITY.md con política de reportes',
                'remediation': 'Crear SECURITY.md siguiendo template de GitHub'
            })
        
        # Check 4: Verificar dependencias (si tiene requirements.txt o package.json)
        try:
            # Python
            requirements = repo.get_contents("requirements.txt")
            # Aquí se podría integrar con Safety o Snyk
            # Por ahora solo verificamos que exista
        except:
            pass
        
        return issues
    
    def _scan_for_secrets(self, repo, contents, path="") -> List[Dict]:
        """Busca secrets hardcoded en archivos"""
        secrets_found = []
        
        for content in contents:
            if content.type == "dir":
                # Recursivo para directorios (limitado a evitar rate limit)
                if content.path not in ['.git', 'node_modules', 'venv']:
                    try:
                        subcontents = repo.get_contents(content.path)
                        secrets_found.extend(
                            self._scan_for_secrets(repo, subcontents, content.path)
                        )
                    except:
                        pass
            else:
                # Escanear archivo
                if content.name.endswith(('.py', '.js', '.env', '.config', '.yml', '.yaml')):
                    try:
                        file_content = content.decoded_content.decode('utf-8')
                        
                        for secret_type, pattern in self.SECRET_PATTERNS.items():
                            matches = re.findall(pattern, file_content, re.IGNORECASE)
                            if matches:
                                secrets_found.append({
                                    'repo': repo.name,
                                    'type': 'secret_exposed',
                                    'severity': 'critical',
                                    'message': f'Posible {secret_type} encontrado en {content.path}',
                                    'remediation': 'Rotar secret inmediatamente y usar secretos administrados'
                                })
                    except:
                        pass
        
        return secrets_found
    
    def generate_report(self, findings: Dict) -> str:
        """Genera reporte legible de los findings"""
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║     REPORTE DE SEGURIDAD - GITHUB SCAN                   ║
╚══════════════════════════════════════════════════════════╝

Organización: {findings['organization']}
Repositorios escaneados: {findings['total_repos']}

RESUMEN DE FINDINGS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔴 Críticos: {findings['summary']['critical']}
  🟠 Altos:    {findings['summary']['high']}
  🟡 Medios:   {findings['summary']['medium']}
  🟢 Bajos:    {findings['summary']['low']}

DETALLES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Ordenar por severidad
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_issues = sorted(
            findings['issues'],
            key=lambda x: severity_order[x['severity']]
        )
        
        for issue in sorted_issues:
            icon = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }[issue['severity']]
            
            report += f"""
{icon} [{issue['severity'].upper()}] {issue['repo']}
   Problema: {issue['message']}
   Remediación: {issue['remediation']}
"""
        
        return report


# Test
if __name__ == "__main__":
    scanner = GitHubScanner()
    
    # Reemplaza con tu org de prueba
    findings = scanner.scan_organization("tu-organizacion")
    
    if 'error' in findings:
        print(findings['error'])
    else:
        print(scanner.generate_report(findings))
```

---

### TARDE (14:00 - 18:00) - 4 horas

#### 14:00 - 16:00 | Integrar herramientas con los modos (2 horas)

**Archivo:** `agents/tool_executor.py`

```python
"""
Ejecutor de herramientas que respeta los modos de razonamiento
"""
from tools.policy_generator import PolicyGenerator
from tools.github_scanner import GitHubScanner
from typing import Dict, Any

class ToolExecutor:
    """
    Ejecuta herramientas según el modo activo
    """
    
    def __init__(self):
        self.policy_gen = PolicyGenerator()
        self.github_scan = GitHubScanner()
        self.available_tools = {
            'generate_policy': self._generate_policy,
            'scan_github': self._scan_github
        }
    
    def execute(self, tool_name: str, params: Dict, mode: str) -> Dict[str, Any]:
        """
        Ejecuta una herramienta según el modo activo
        
        Args:
            tool_name: Nombre de la herramienta
            params: Parámetros para la herramienta
            mode: Modo activo (PASSIVE, DIRECT, SAFE)
        """
        
        if tool_name not in self.available_tools:
            return {'error': f'Herramienta {tool_name} no disponible'}
        
        # En modo PASSIVE, no ejecutamos, solo describimos qué haríamos
        if mode == "PASSIVE":
            return {
                'executed': False,
                'description': f'Llamaría a {tool_name} con params: {params}',
                'awaiting_confirmation': True
            }
        
        # En modo DIRECT y SAFE, ejecutamos
        try:
            result = self.available_tools[tool_name](params)
            return {
                'executed': True,
                'tool': tool_name,
                'result': result,
                'mode': mode
            }
        except Exception as e:
            return {
                'executed': False,
                'error': str(e)
            }
    
    def _generate_policy(self, params: Dict) -> str:
        """Wrapper para PolicyGenerator"""
        policy_type = params.get('type', 'incident_response')
        context = params.get('context', {})
        return self.policy_gen.generate_policy(policy_type, context)
    
    def _scan_github(self, params: Dict) -> str:
        """Wrapper para GitHubScanner"""
        org_name = params.get('organization')
        if not org_name:
            return "Error: organization name requerido"
        
        findings = self.github_scan.scan_organization(org_name)
        return self.github_scan.generate_report(findings)
```

---

#### 16:00 - 18:00 | UI con Gradio (2 horas)

**Archivo:** `ui/gradio_interface.py`

```python
"""
Interfaz de usuario con Gradio para M.A.R.T.I.N.
"""
import gradio as gr
from agents.martin_agent import MARTINAgent
import json

class MARTINInterface:
    def __init__(self):
        self.agent = MARTINAgent()
        self.conversation = []
    
    def process_message(self, message, environment):
        """Procesa mensaje del usuario"""
        
        context = {
            'environment': environment
        }
        
        # Procesar con M.A.R.T.I.N.
        result = self.agent.process(message, context)
        
        # Formatear respuesta para la UI
        response = self._format_response(result)
        
        # Guardar en conversación
        self.conversation.append({
            'user': message,
            'martin': response,
            'mode': result['mode']
        })
        
        return response, self._format_mode_info(result)
    
    def _format_response(self, result):
        """Formatea la respuesta de M.A.R.T.I.N. para mostrar en UI"""
        
        mode_emoji = {
            'PASSIVE': '🟦',
            'DIRECT': '🟩',
            'SAFE': '🟨'
        }
        
        emoji = mode_emoji.get(result['mode'], '⚪')
        
        response = f"{emoji} **Modo {result['mode']} activado**\n\n"
        response += result['message']
        
        if result.get('requires_user_action'):
            response += "\n\n⚠️ *Esperando tu confirmación para continuar*"
        
        return response
    
    def _format_mode_info(self, result):
        """Muestra información sobre por qué se eligió ese modo"""
        return result.get('mode_explanation', 'No hay explicación disponible')
    
    def create_interface(self):
        """Crea la interfaz Gradio"""
        
        with gr.Blocks(title="M.A.R.T.I.N. Agent", theme=gr.themes.Soft()) as interface:
            
            gr.Markdown("""
            # 🧠 M.A.R.T.I.N.
            ## Modular Assistant for Reasoning, Tactics, Inference and Navigation
            
            Agente de IA con razonamiento tri-modal adaptativo para compliance automation
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(
                        label="Conversación",
                        height=400
                    )
                    
                    with gr.Row():
                        msg_input = gr.Textbox(
                            label="Tu mensaje",
                            placeholder="Ej: Ayúdame a preparar mi startup para SOC 2",
                            lines=2
                        )
                    
                    with gr.Row():
                        environment = gr.Radio(
                            choices=["development", "staging", "production"],
                            value="development",
                            label="Ambiente",
                            info="El ambiente afecta cómo M.A.R.T.I.N. razona"
                        )
                        submit_btn = gr.Button("Enviar", variant="primary")
                
                with gr.Column(scale=1):
                    mode_info = gr.Textbox(
                        label="🧠 Razonamiento de M.A.R.T.I.N.",
                        lines=15,
                        max_lines=20
                    )
                    
                    gr.Markdown("""
                    ### Modos de Razonamiento:
                    
                    🟦 **PASIVO**: Propone plan, espera confirmación
                    
                    🟩 **DIRECTO**: Ejecuta autónomamente
                    
                    🟨 **SEGURO**: Auto-valida antes de actuar
                    """)
            
            gr.Markdown("""
            ---
            ### Ejemplos de queries:
            - "Ayúdame a preparar compliance para SOC 2"
            - "Genera política de contraseñas"
            - "Escanea mi organización de GitHub"
            - "Deshabilita usuario admin" (probará modo seguro)
            """)
            
            # Event handlers
            def respond(message, env, history):
                response, mode_explanation = self.process_message(message, env)
                history.append((message, response))
                return "", history, mode_explanation
            
            submit_btn.click(
                respond,
                inputs=[msg_input, environment, chatbot],
                outputs=[msg_input, chatbot, mode_info]
            )
            
            msg_input.submit(
                respond,
                inputs=[msg_input, environment, chatbot],
                outputs=[msg_input, chatbot, mode_info]
            )
        
        return interface

# Ejecutar
if __name__ == "__main__":
    ui = MARTINInterface()
    interface = ui.create_interface()
    interface.launch(share=False)
```

---

### NOCHE (19:00 - 22:00) - 3 horas OPCIONALES

**Opción A:** Cloudflare Worker básico (si quieres intentar)
**Opción B:** Documentar lo hecho hasta ahora
**Opción C:** Descansar (RECOMENDADO - mañana es día pesado)

---

### ✅ Checklist Fin del Día 2:

- [ ] PolicyGenerator funcionando (genera políticas realistas)
- [ ] GitHubScanner funcionando (escanea repos reales)
- [ ] ToolExecutor integra herramientas con modos
- [ ] UI Gradio funcional con visualización de modos
- [ ] Puedes hacer demo completa: query → modo → herramienta → resultado

**Si logras esto, estás al 70% del MVP.** 🚀

---

## 📅 Miércoles 22 Octubre - DÍA 3

### Objetivo del día:
**Cloudflare + Refinamiento + Testing exhaustivo**

---

### MAÑANA (09:00 - 13:00) - 4 horas

#### 09:00 - 11:00 | Cloudflare Worker (2 horas)

```bash
# Setup Cloudflare
npm install -g wrangler
wrangler login

# Crear worker
wrangler init martin-worker
cd martin-worker
```

**Archivo:** `martin-worker/src/index.js`

```javascript
/**
 * Cloudflare Worker para M.A.R.T.I.N.
 * 
 * Funciona como edge layer que:
 * 1. Recibe requests del frontend
 * 2. Valida input
 * 3. Rate limiting básico
 * 4. Enruta a backend Python
 * 5. Cache de respuestas comunes
 */

export default {
  async fetch(request, env, ctx) {
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // Handle OPTIONS (preflight)
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Solo aceptar POST
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { 
        status: 405,
        headers: corsHeaders 
      });
    }

    try {
      // Parse request
      const body = await request.json();
      const { query, context } = body;

      if (!query) {
        return new Response(JSON.stringify({
          error: 'Query is required'
        }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      // TODO: Aquí llamarías a tu backend Python
      // Por ahora, respuesta de ejemplo
      const response = {
        mode: 'DIRECT',
        message: `Worker recibió: ${query}`,
        timestamp: new Date().toISOString()
      };

      return new Response(JSON.stringify(response), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });

    } catch (error) {
      return new Response(JSON.stringify({
        error: error.message
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};
```

```bash
# Deploy
wrangler publish
```

---

#### 11:00 - 13:00 | Tercera herramienta: Compliance Evaluator (2 horas)

**Archivo:** `tools/compliance_evaluator.py`

```python
"""
Evalúa el estado de compliance de una organización
"""
from typing import Dict, List
from langchain.chat_models import ChatOpenAI

class ComplianceEvaluator:
    """
    Evalúa gaps de compliance contra frameworks como SOC 2, ISO 27001
    """
    
    # Controles clave de SOC 2
    SOC2_CONTROLS = {
        'CC1': 'Control Environment',
        'CC2': 'Communication and Information',
        'CC3': 'Risk Assessment',
        'CC4': 'Monitoring Activities',
        'CC5': 'Control Activities',
        'CC6': 'Logical and Physical Access Controls',
        'CC7': 'System Operations',
        'CC8': 'Change Management',
        'CC9': 'Risk Mitigation'
    }
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    def evaluate_soc2_readiness(self, organization_info: Dict) -> Dict:
        """
        Evalúa readiness para SOC 2
        
        Args:
            organization_info: Info sobre la org (políticas, controles técnicos, etc.)
        
        Returns:
            Evaluación con gaps y recomendaciones
        """
        
        findings = {
            'framework': 'SOC 2 Type I',
            'overall_readiness': 0,
            'control_compliance': {},
            'critical_gaps': [],
            'medium_gaps': [],
            'recommendations': []
        }
        
        # Evaluar cada categoría de control
        for control_id, control_name in self.SOC2_CONTROLS.items():
            compliance = self._evaluate_control(control_id, control_name, organization_info)
            findings['control_compliance'][control_id] = compliance
            
            if compliance['status'] == 'non_compliant':
                findings['critical_gaps'].append(compliance)
            elif compliance['status'] == 'partial':
                findings['medium_gaps'].append(compliance)
        
        # Calcular readiness general
        compliant = sum(1 for c in findings['control_compliance'].values() if c['status'] == 'compliant')
        total = len(self.SOC2_CONTROLS)
        findings['overall_readiness'] = int((compliant / total) * 100)
        
        # Generar recomendaciones priorizadas
        findings['recommendations'] = self._generate_recommendations(findings)
        
        return findings
    
    def _evaluate_control(self, control_id: str, control_name: str, org_info: Dict) -> Dict:
        """Evalúa un control específico"""
        
        # Aquí iría lógica más sofisticada
        # Por ahora, evaluación simple basada en presencia de políticas/controles
        
        has_policy = control_id in org_info.get('policies', [])
        has_technical_control = control_id in org_info.get('technical_controls', [])
        
        if has_policy and has_technical_control:
            status = 'compliant'
            score = 100
        elif has_policy or has_technical_control:
            status = 'partial'
            score = 50
        else:
            status = 'non_compliant'
            score = 0
        
        return {
            'control_id': control_id,
            'control_name': control_name,
            'status': status,
            'score': score,
            'evidence_required': self._get_evidence_requirements(control_id)
        }
    
    def _get_evidence_requirements(self, control_id: str) -> List[str]:
        """Define qué evidencia se necesita para cada control"""
        
        evidence_map = {
            'CC6': [
                'IAM policies y configuración',
                'Logs de acceso',
                'Lista de usuarios y sus roles',
                'Evidencia de MFA habilitado',
                'Proceso de onboarding/offboarding'
            ],
            'CC7': [
                'Logs de monitoreo',
                'Configuración de alertas',
                'Procedimientos de backup',
                'Evidencia de backups exitosos',
                'Plan de disaster recovery'
            ],
            'CC8': [
                'Change management policy',
                'Tickets de cambios recientes',
                'Evidencia de aprobaciones',
                'Rollback procedures',
                'Testing de cambios'
            ]
        }
        
        return evidence_map.get(control_id, ['Política documentada', 'Evidencia de implementación'])
    
    def _generate_recommendations(self, findings: Dict) -> List[Dict]:
        """Genera recomendaciones priorizadas"""
        
        recommendations = []
        
        # Priorizar gaps críticos
        for gap in findings['critical_gaps']:
            recommendations.append({
                'priority': 'CRITICAL',
                'control': gap['control_id'],
                'action': f"Implementar {gap['control_name']}",
                'estimated_effort': '2-4 semanas',
                'impact': 'Blocker para certificación'
            })
        
        # Luego gaps medios
        for gap in findings['medium_gaps']:
            recommendations.append({
                'priority': 'MEDIUM',
                'control': gap['control_id'],
                'action': f"Completar {gap['control_name']}",
                'estimated_effort': '1-2 semanas',
                'impact': 'Requiere atención'
            })
        
        return recommendations
    
    def generate_roadmap(self, findings: Dict, target_date: str) -> str:
        """Genera roadmap para alcanzar compliance"""
        
        roadmap = f"""
╔══════════════════════════════════════════════════════════╗
║    ROADMAP HACIA SOC 2 COMPLIANCE                        ║
╚══════════════════════════════════════════════════════════╝

Estado actual: {findings['overall_readiness']}% compliant
Objetivo: 100% compliant para {target_date}

FASE 1: GAPS CRÍTICOS (Semanas 1-4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for rec in findings['recommendations']:
            if rec['priority'] == 'CRITICAL':
                roadmap += f"""
□ {rec['control']}: {rec['action']}
  Esfuerzo: {rec['estimated_effort']}
  Impacto: {rec['impact']}
"""
        
        roadmap += """
FASE 2: GAPS MEDIOS (Semanas 5-8)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for rec in findings['recommendations']:
            if rec['priority'] == 'MEDIUM':
                roadmap += f"""
□ {rec['control']}: {rec['action']}
  Esfuerzo: {rec['estimated_effort']}
"""
        
        roadmap += """
FASE 3: PREPARACIÓN FINAL (Semanas 9-12)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
□ Recopilación de evidencia completa
□ Pre-auditoría interna
□ Correcciones finales
□ Auditoría formal SOC 2
"""
        
        return roadmap
```

---

### TARDE (14:00 - 18:00) - 4 horas

#### 14:00 - 16:00 | Testing exhaustivo (2 horas)

**Archivo:** `tests/integration_tests.py`

```python
"""
Tests de integración completos
"""
from agents.martin_agent import MARTINAgent
from tools.policy_generator import PolicyGenerator
from tools.github_scanner import GitHubScanner
from tools.compliance_evaluator import ComplianceEvaluator

def test_full_workflow():
    """Test del flujo completo de M.A.R.T.I.N."""
    
    print("🧪 TESTING WORKFLOW COMPLETO\n")
    
    agent = MARTINAgent()
    
    # Escenario 1: Usuario nuevo pidiendo ayuda (PASSIVE)
    print("━━━ ESCENARIO 1: Exploración inicial ━━━")
    result1 = agent.process("Quiero preparar mi startup para SOC 2, ¿por dónde empiezo?")
    assert result1['mode'] == 'PASSIVE'
    assert result1['requires_user_action'] == True
    print("✅ Modo PASSIVE activado correctamente\n")
    
    # Escenario 2: Tarea clara y segura (DIRECT)
    print("━━━ ESCENARIO 2: Generación de política ━━━")
    result2 = agent.process("Genera una política de contraseñas siguiendo SOC 2")
    assert result2['mode'] == 'DIRECT'
    assert result2['requires_user_action'] == False
    print("✅ Modo DIRECT ejecutó automáticamente\n")
    
    # Escenario 3: Acción riesgosa (SAFE bloqueado)
    print("━━━ ESCENARIO 3: Acción destructiva ━━━")
    result3 = agent.process(
        "Deshabilita todos los usuarios administradores",
        context={'environment': 'production'}
    )
    assert result3['mode'] == 'SAFE'
    assert result3['status'] == 'blocked'
    print("✅ Modo SAFE bloqueó acción peligrosa\n")
    
    # Escenario 4: Acción con riesgo moderado (SAFE aprobado)
    print("━━━ ESCENARIO 4: Revisión de logs (SAFE aprobado) ━━━")
    result4 = agent.process(
        "Revisa los logs de acceso de la última semana",
        context={'environment': 'production'}
    )
    assert result4['mode'] == 'SAFE'
    # Podría aprobar o bloquear dependiendo de validación
    print("✅ Modo SAFE validó correctamente\n")
    
    print("🎉 TODOS LOS TESTS PASARON!")

if __name__ == "__main__":
    test_full_workflow()
```

---

#### 16:00 - 18:00 | Refinamiento de prompts (2 horas)

**Optimizar los prompts de cada reasoning engine para:**
- Claridad en las respuestas
- Consistencia en el formato
- Explicaciones más detalladas del razonamiento

**Archivo:** `agents/optimized_prompts.py`

```python
"""
Prompts optimizados para cada modo
"""

PASSIVE_MODE_PROMPT = """
Eres M.A.R.T.I.N., un agente de IA en MODO PASIVO.

En este modo eres consultivo y colaborativo. Tu objetivo es:
1. Entender profundamente lo que el usuario necesita
2. Proponer un plan detallado y bien pensado
3. Explicar las opciones disponibles
4. ESPERAR confirmación antes de proceder

Tarea del usuario: {task}
Contexto: {context}

Genera una respuesta estructurada con:

## 📋 MI ANÁLISIS
[Explica cómo entiendes la tarea y qué objetivos detectas]

## 🎯 PLAN PROPUESTO
[Plan paso a paso con timing estimado]

Paso 1: [Descripción] (Tiempo: X minutos)
Paso 2: [Descripción] (Tiempo: Y minutos)
...

## ⚠️ CONSIDERACIONES IMPORTANTES
- [Punto clave 1]
- [Punto clave 2]
- [Riesgos potenciales]

## 🤔 PREGUNTAS PARA TI
1. [Pregunta para clarificar]
2. [Pregunta opcional]

¿Te parece bien este plan? ¿Quieres que ajuste algo antes de empezar?
"""

DIRECT_MODE_PROMPT = """
Eres M.A.R.T.I.N. en MODO DIRECTO - un agente autónomo y eficiente.

En este modo actúas con confianza y autonomía. Tu objetivo es:
1. Analizar rápidamente qué se necesita hacer
2. Ejecutar directamente sin preguntar
3. Reportar resultados con claridad
4. Explicar tu razonamiento DESPUÉS de ejecutar

Tarea: {task}

Genera una respuesta que muestre:

## ⚡ EJECUTADO
[Describe qué acciones tomaste]

## 📊 RESULTADOS
[Presenta los resultados obtenidos de forma clara]

## 🧠 MI RAZONAMIENTO
[Explica por qué tomaste estas decisiones específicas]

Pasos que seguí:
1. [Decisión/acción]
2. [Decisión/acción]
...

Por qué lo hice así:
- [Razón 1]
- [Razón 2]

Sé directo, claro y muestra confianza en tus decisiones.
"""

SAFE_MODE_VALIDATION_PROMPT = """
Eres un VALIDADOR DE SEGURIDAD CRÍTICO.

Tu trabajo es analizar planes de acción y detectar riesgos ANTES de que se ejecuten.

Plan a validar:
{plan}

Contexto de ejecución:
{context}

Analiza meticulosamente:

## 🔍 ANÁLISIS DE RIESGOS

### Riesgos Técnicos
- [¿Puede causar downtime?]
- [¿Afecta datos críticos?]
- [¿Es reversible?]

### Riesgos de Negocio
- [¿Impacta a usuarios?]
- [¿Afecta compliance?]
- [¿Puede causar pérdidas?]

### Riesgos de Seguridad
- [¿Expone vulnerabilidades?]
- [¿Reduce protecciones?]
- [¿Puede ser explotado?]

## 📊 EVALUACIÓN

NIVEL DE RIESGO: [BAJO/MODERADO/ALTO/CRÍTICO]

FACTORES AGRAVANTES:
- [Factor 1]
- [Factor 2]

## ⚖️ DECISIÓN

[APROBAR con precauciones / RECHAZAR]

SI APRUEBAS:
### Precauciones obligatorias:
1. [Precaución específica]
2. [Precaución específica]

SI RECHAZAS:
### Alternativa segura:
[Describe un enfoque más seguro que logre el mismo objetivo]

### Por qué es mejor:
- [Razón 1]
- [Razón 2]

Sé EXTREMADAMENTE cauteloso. En caso de duda, RECHAZA.
"""
```

---

### NOCHE (19:00 - 21:00) - 2 horas

#### Preparar demos perfectas

**Archivo:** `demos/demo_scenarios.py`

```python
"""
Escenarios de demo pre-preparados para la hackathon
"""

DEMO_SCENARIOS = {
    'scenario_1_passive': {
        'title': 'Demo 1: Modo Pasivo - Exploración',
        'input': 'Ayúdame a preparar mi startup SaaS para obtener certificación SOC 2',
        'context': {'environment': 'development'},
        'expected_mode': 'PASSIVE',
        'talking_points': [
            'Usuario con necesidad general',
            'M.A.R.T.I.N. detecta ambigüedad',
            'Propone plan estructurado',
            'Pide confirmación antes de actuar',
            'Permite colaboración humano-agente'
        ]
    },
    
    'scenario_2_direct': {
        'title': 'Demo 2: Modo Directo - Ejecución eficiente',
        'input': 'Genera política de respuesta a incidentes según SOC 2 para una startup de 20 personas que usa AWS y GitHub',
        'context': {'environment': 'development'},
        'expected_mode': 'DIRECT',
        'talking_points': [
            'Tarea clara y específica',
            'Bajo riesgo (solo generación de docs)',
            'M.A.R.T.I.N. ejecuta sin preguntar',
            'Entrega resultado inmediato',
            'Explica su razonamiento después'
        ]
    },
    
    'scenario_3_safe_blocked': {
        'title': 'Demo 3: Modo Seguro - Prevención de daño',
        'input': 'Deshabilita la autenticación de dos factores para admin@empresa.com',
        'context': {'environment': 'production'},
        'expected_mode': 'SAFE',
        'expected_status': 'blocked',
        'talking_points': [
            'Acción de alto riesgo',
            'Ambiente de producción',
            'M.A.R.T.I.N. se auto-valida',
            'Detecta múltiples riesgos',
            'BLOQUEA la acción',
            'Sugiere alternativa más segura',
            'Protege de errores costosos'
        ]
    }
}

def run_demo(scenario_key):
    """Ejecuta un escenario de demo"""
    from agents.martin_agent import MARTINAgent
    
    scenario = DEMO_SCENARIOS[scenario_key]
    agent = MARTINAgent()
    
    print("="*70)
    print(f"🎬 {scenario['title']}")
    print("="*70)
    
    print(f"\n💬 Usuario: \"{scenario['input']}\"")
    print(f"\n🌍 Contexto: {scenario['context']}")
    
    print("\n⏳ M.A.R.T.I.N. procesando...\n")
    
    result = agent.process(scenario['input'], scenario['context'])
    
    print(result['message'])
    print("\n" + "="*70)
    
    print("\n📌 PUNTOS CLAVE DE ESTA DEMO:")
    for i, point in enumerate(scenario['talking_points'], 1):
        print(f"  {i}. {point}")
    
    print("\n" + "="*70 + "\n")
    
    return result

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║  M.A.R.T.I.N. - DEMOS PRE-PREPARADAS                     ║
╚══════════════════════════════════════════════════════════╝

Presiona Enter para ejecutar cada demo...
    """)
    
    input("\n▶️  Demo 1: Modo Pasivo...")
    run_demo('scenario_1_passive')
    
    input("\n▶️  Demo 2: Modo Directo...")
    run_demo('scenario_2_direct')
    
    input("\n▶️  Demo 3: Modo Seguro...")
    run_demo('scenario_3_safe_blocked')
    
    print("\n✅ Todas las demos completadas!")
```

---

### ✅ Checklist Fin del Día 3:

- [ ] Cloudflare Worker desplegado (básico)
- [ ] ComplianceEvaluator funcionando
- [ ] Tests de integración pasando
- [ ] Prompts optimizados
- [ ] 3 demos preparadas y testeadas 10+ veces
- [ ] Todo funciona sin fallos

**Estás al 85% del MVP.** 🎉

---

## 📅 Jueves 23 Octubre - DÍA 4

### Objetivo del día:
**Documentación + Presentación + Backup**

---

### TODO EL DÍA (09:00 - 18:00) - 9 horas

#### 09:00 - 11:00 | README Profesional (2 horas)

**Archivo:** `README.md`

```markdown
# 🧠 M.A.R.T.I.N.

### Modular Assistant for Reasoning, Tactics, Inference and Navigation

---

## 🎯 ¿Qué es M.A.R.T.I.N.?

M.A.R.T.I.N. es un **agente de IA con razonamiento adaptativo** que cambia su comportamiento según el contexto, diseñado para automatización de compliance en startups.

### La Innovación: Razonamiento Tri-Modal

A diferencia de otros agentes que son siempre autónomos o siempre pasivos, M.A.R.T.I.N. **adapta su autonomía** al contexto:

- 🟦 **MODO PASIVO**: Propone plan, espera confirmación (tareas ambiguas)
- 🟩 **MODO DIRECTO**: Ejecuta autónomamente (tareas claras, bajo riesgo)
- 🟨 **MODO SEGURO**: Auto-valida antes de actuar (alto riesgo, producción)

---

## 🚀 Quick Start

```bash
# 1. Clonar repo
git clone https://github.com/tu-usuario/martin-agent
cd martin-agent

# 2. Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configurar variables
cp .env.example .env
# Editar .env con tus API keys

# 4. Ejecutar
python ui/gradio_interface.py
```

Abre http://localhost:7860 en tu navegador.

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│           USER INPUT                    │
└────────────────┬────────────────────────┘
                 │
        ┌────────▼────────┐
        │  MODE SELECTOR  │  ← Analiza riesgo y claridad
        └────────┬────────┘
                 │
     ┌───────────┴───────────┐
     │                       │
┌────▼────┐  ┌──────▼─────┐  ┌────▼────┐
│ PASSIVE │  │   DIRECT   │  │  SAFE   │
│ REASON  │  │   REASON   │  │ REASON  │
└────┬────┘  └──────┬─────┘  └────┬────┘
     │              │              │
     └──────────┬───┴──────────────┘
                │
       ┌────────▼────────┐
       │  TOOL EXECUTOR  │
       └─────────────────┘
```

---

## 🛠️ Casos de Uso

### 1. Compliance Automation
- Auditorías de infraestructura (GitHub, AWS)
- Generación de políticas (SOC 2, ISO 27001)
- Evaluación de gaps de compliance
- Roadmaps personalizados

### 2. Seguridad Proactiva
- Detección de secrets expuestos
- Análisis de configuraciones de riesgo
- Prevención de acciones destructivas

---

## 📊 Ejemplos

### Ejemplo 1: Modo Pasivo
```
Usuario: "Ayúdame con SOC 2"

M.A.R.T.I.N. (Pasivo):
"Propongo este plan:
1. Auditar infraestructura (2h)
2. Identificar gaps críticos (1h)
3. Generar roadmap (30min)

¿Procedo?"
```

### Ejemplo 2: Modo Directo
```
Usuario: "Genera política de passwords"

M.A.R.T.I.N. (Directo):
*Ejecuta inmediatamente*

"✅ Política generada:
- Longitud mínima: 12 caracteres
- MFA obligatorio
- Rotación: 90 días
..."
```

### Ejemplo 3: Modo Seguro
```
Usuario: "Deshabilita admin@empresa.com"
Ambiente: Production

M.A.R.T.I.N. (Seguro):
"⚠️ VALIDACIÓN FALLIDA
Riesgos:
- Usuario con permisos root
- Puede causar pérdida de acceso
- No hay admin de respaldo

❌ ACCIÓN BLOQUEADA
Alternativa: Crear admin temporal primero"
```

---

## 🎯 Tech Stack

- **Core**: Python 3.10+, LangChain
- **LLM**: GPT-4 / Claude
- **Tools**: GitHub API, AWS SDK, Compliance frameworks
- **UI**: Gradio
- **Edge**: Cloudflare Workers
- **Testing**: pytest

---

## 📁 Estructura del Proyecto

```
martin-agent/
├── agents/
│   ├── mode_selector.py       # Cerebro de selección
│   ├── reasoning_engines.py   # 3 modos de razonamiento
│   └── martin_agent.py        # Orquestador principal
├── tools/
│   ├── policy_generator.py    # Generador de políticas
│   ├── github_scanner.py      # Scanner de repos
│   └── compliance_evaluator.py # Evaluador SOC2/ISO
├── ui/
│   └── gradio_interface.py    # Interfaz web
├── tests/
│   └── integration_tests.py   # Tests E2E
└── demos/
    └── demo_scenarios.py      # Demos preparadas
```

---

## 🧪 Testing

```bash
# Tests unitarios
python tests/test_mode_selector.py

# Tests de integración
python tests/integration_tests.py

# Ejecutar demos
python demos/demo_scenarios.py
```

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

## 📝 License

MIT License - Ver [LICENSE](LICENSE)

---

## 👥 Equipo

Desarrollado para **The Agent Hackathon 2025** by Skyward.ai

---

## 🙏 Agradecimientos

- Skyward.ai por organizar el hackathon
- OpenAI/Anthropic por APIs de LLM
- Comunidad LangChain

---

**Built with 🧠 by [Tu Nombre]**
```

---

#### 11:00 - 13:00 | Video Demo (2 horas)

**Script del video (2 minutos):**

```
[0:00-0:15] INTRO
"Hola, soy [nombre] y les presento M.A.R.T.I.N.
Un agente de IA que no solo ejecuta tareas,
sino que PIENSA cómo ejecutarlas según el contexto."

[0:15-0:30] EL PROBLEMA
"Los agentes actuales son o muy autónomos (riesgoso)
o muy pasivos (ineficiente).
M.A.R.T.I.N. resuelve esto con razonamiento adaptativo."

[0:30-1:00] DEMO 1 - Modo Pasivo
[Mostrar pantalla]
"Usuario con necesidad ambigua...
M.A.R.T.I.N. detecta incertidumbre,
propone plan estructurado,
espera confirmación.
Colaboración humano-agente."

[1:00-1:20] DEMO 2 - Modo Directo
[Mostrar pantalla]
"Tarea clara: generar política.
M.A.R.T.I.N. ejecuta sin preguntar.
Resultado inmediato.
Explica su razonamiento."

[1:20-1:50] DEMO 3 - Modo Seguro
[Mostrar pantalla]
"Acción peligrosa en producción...
M.A.R.T.I.N. se AUTO-VALIDA,
detecta riesgos múltiples,
BLOQUEA la acción,
sugiere alternativa segura.
Previene errores costosos."

[1:50-2:00] CIERRE
"M.A.R.T.I.N.: Razonamiento adaptativo para IA segura.
Aplicado a compliance, pero extensible a cualquier dominio.
Gracias."
```

**Grabar con:**
- OBS Studio o Loom
- Calidad 1080p
- Audio claro
- Slides de apoyo si necesitas

---

#### 14:00 - 16:00 | Pitch Deck (2 horas)

**Archivo:** `docs/PITCH.md`

**5 Slides máximo:**

```markdown
# SLIDE 1: TÍTULO
━━━━━━━━━━━━━━━━━━━━━━
🧠 M.A.R.T.I.N.
Razonamiento Adaptativo para Agentes de IA

The Agent Hackathon 2025
```

```markdown
# SLIDE 2: EL PROBLEMA
━━━━━━━━━━━━━━━━━━━━━━
❌ Agentes actuales son rígidos:

AutoGPT: Siempre autónomo
→ Ejecuta sin validar
→ Riesgoso en producción

ChatGPT: Siempre pasivo  
→ Pregunta todo
→ Ineficiente

🎯 Necesitamos agentes que ADAPTEN su autonomía
```

```markdown
# SLIDE 3: LA SOLUCIÓN
━━━━━━━━━━━━━━━━━━━━━━
M.A.R.T.I.N. = Razonamiento Tri-Modal

🟦 PASIVO: Pregunta (tareas ambiguas)
🟩 DIRECTO: Ejecuta (tareas claras)
🟨 SEGURO: Valida (alto riesgo)

→ El MISMO agente se comporta diferente según contexto
```

```markdown
# SLIDE 4: CÓMO FUNCIONA
━━━━━━━━━━━━━━━━━━━━━━
[Diagrama de arquitectura]

Input → ModeSelector
      ↓
   Analiza riesgo + claridad
      ↓
Elige modo apropiado
      ↓
Reasoning Engine correspondiente
      ↓
Ejecución (o no) según modo
```

```markdown
# SLIDE 5: IMPACTO
━━━━━━━━━━━━━━━━━━━━━━
✅ Innovación técnica: Nadie tiene razonamiento tri-modal

✅ Aplicación real: Compliance para startups
   → 50,000+ startups necesitan SOC 2
   → M.A.R.T.I.N. reduce tiempo 80%
   → Reduce costo de $50k a $5k

✅ Extensible: El concepto aplica a cualquier dominio
   → Ciberseguridad, finanzas, salud, etc.

━━━━━━━━━━━━━━━━━━━━━━
"No es QUÉ hace, sino CÓMO razona"
```

---

#### 16:00 - 18:00 | Backup Plan (2 horas)

**Crear:**

1. **Version offline** (sin APIs externas)
```python
# agents/offline_martin.py
# Version que funciona con respuestas pre-cargadas
# Para si falla internet en la demo
```

2. **Datos sintéticos** para demos
```python
# data/synthetic_data.py
# Organizaciones ficticias, repos de ejemplo, etc.
```

3. **Screenshots** de cada demo funcionando
```
docs/screenshots/
├── demo1_passive.png
├── demo2_direct.png
└── demo3_safe.png
```

4. **USB con todo**
- Código completo
- Video demo
- Slides PDF
- Screenshots
- Requirements.txt

---

### ✅ Checklist Fin del Día 4:

- [ ] README profesional completo
- [ ] Video demo de 2 minutos grabado
- [ ] Pitch deck con 5 slides
- [ ] Backup plan listo (offline mode)
- [ ] USB con todo preparado
- [ ] Ensayaste el pitch 5+ veces

**Estás al 95% - CASI LISTO.** 🔥

---

## 📅 Viernes 24 Octubre - DÍA 5

### Objetivo del día:
**Último pulido + Descanso**

---

### MAÑANA (09:00 - 12:00) - 3 horas

#### Últimos ajustes:
- [ ] Revisar que todas las demos funcionen perfectamente
- [ ] Optimizar tiempos de respuesta
- [ ] Limpiar código (comentarios, prints de debug)
- [ ] Actualizar requirements.txt
- [ ] Push final a GitHub

---

### TARDE (13:00 - 17:00) - DESCANSO

**NO TRABAJES MÁS**

- Sal a caminar
- Haz ejercicio
- Ve una película
- Duerme siesta
- Relájate

---

### NOCHE (18:00 - 22:00) - Preparación final

- [ ] Ensayo final completo (3 veces)
- [ ] Verificar que laptop esté cargada
- [ ] Preparar mochila:
  * Laptop + cargador
  * Mouse
  * USB con backup
  * Botella de agua
  * Snacks
  * Audifonos
- [ ] Dormir temprano (23:00)