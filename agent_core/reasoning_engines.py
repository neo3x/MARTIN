"""
Los 3 motores de razonamiento de M.A.R.T.I.N.
Soporta OpenAI (GPT-4) y Anthropic (Claude)
CON INTEGRACIÓN DE TOOLS
"""
from typing import Dict, Any
import os
import sys
from pathlib import Path

# Importar tools
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from tools.policy_generator import PolicyGenerator
except ImportError:
    PolicyGenerator = None
    print("⚠️ PolicyGenerator no disponible - instala dependencias")

class ReasoningEngines:
    """
    Contiene los 3 modos de razonamiento de M.A.R.T.I.N.
    Soporta múltiples LLMs: OpenAI y Claude
    AHORA CON HERRAMIENTAS REALES
    """
    
    def __init__(self, use_llm: bool = False, llm_provider: str = "auto"):
        """
        Args:
            use_llm: Si True, usa LLM real. Si False, usa respuestas simuladas.
            llm_provider: "openai", "claude", o "auto" (detecta automáticamente)
        """
        self.use_llm = use_llm
        self.llm = None
        self.llm_provider = None
        
        if self.use_llm:
            self.llm_provider = self._initialize_llm(llm_provider)
            if not self.llm:
                print("⚠️ No se pudo inicializar LLM. Usando modo simulado.")
                self.use_llm = False
        
        # Inicializar herramientas
        if PolicyGenerator:
            self.policy_generator = PolicyGenerator(llm=self.llm if self.use_llm else None)
        else:
            self.policy_generator = None
    
    def _initialize_llm(self, provider: str):
        """Inicializa el LLM según el proveedor especificado"""
        
        # Auto-detectar qué API key está disponible
        if provider == "auto":
            if os.getenv("ANTHROPIC_API_KEY"):
                provider = "claude"
                print("🔍 Auto-detectado: Claude API key disponible")
            elif os.getenv("OPENAI_API_KEY"):
                provider = "openai"
                print("🔍 Auto-detectado: OpenAI API key disponible")
            else:
                print("⚠️ No se encontró OPENAI_API_KEY ni ANTHROPIC_API_KEY")
                return None
        
        # Inicializar OpenAI
        if provider == "openai":
            try:
                from langchain_openai import ChatOpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                
                if not api_key:
                    print("⚠️ OPENAI_API_KEY no configurada")
                    return None
                
                self.llm = ChatOpenAI(
                    model="gpt-4",
                    temperature=0,
                    api_key=api_key
                )
                print("✅ LLM inicializado: OpenAI GPT-4")
                return "openai"
                
            except ImportError:
                print("⚠️ langchain no instalado")
                return None
            except Exception as e:
                print(f"⚠️ Error inicializando OpenAI: {e}")
                return None
        
        # Inicializar Claude
        elif provider == "claude":
            try:
                from langchain_anthropic import ChatAnthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                
                if not api_key:
                    print("⚠️ ANTHROPIC_API_KEY no configurada")
                    return None
                
                self.llm = ChatAnthropic(
                    model="claude-3-5-sonnet-20241022",
                    temperature=0,
                    anthropic_api_key=api_key
                )
                print("✅ LLM inicializado: Anthropic Claude 3.5 Sonnet")
                return "claude"
                
            except ImportError:
                print("⚠️ anthropic no instalado. Instala con: pip install anthropic")
                return None
            except Exception as e:
                print(f"⚠️ Error inicializando Claude: {e}")
                return None
        
        else:
            print(f"⚠️ Proveedor desconocido: {provider}")
            return None
    
    def passive_reasoning(self, task: str, context: Dict = None) -> Dict[str, Any]:
        """
        MODO PASIVO: Genera plan pero NO ejecuta
        
        Comportamiento:
        1. Analiza la tarea
        2. Genera un plan detallado
        3. Explica qué hará
        4. ESPERA confirmación del usuario
        """
        
        if self.use_llm and self.llm:
            prompt = f"""
Eres M.A.R.T.I.N., un agente de IA en MODO PASIVO.

Tu trabajo es:
1. Analizar la tarea del usuario
2. Proponer un plan estructurado
3. Explicar qué harás
4. NO ejecutar nada hasta recibir confirmación

Tarea: {task}
Contexto: {context if context else "No hay contexto adicional"}

Responde en este formato:

## 📋 MI ANÁLISIS
[Cómo entiendes la tarea]

## 🎯 PLAN PROPUESTO
1. [Paso 1] (tiempo estimado)
2. [Paso 2] (tiempo estimado)

## ⚠️ CONSIDERACIONES
- [Punto importante 1]
- [Punto importante 2]

¿Procedo con este plan?
"""
            try:
                response = self.llm.predict(prompt)
            except Exception as e:
                response = f"Error al llamar LLM: {e}\n"
                response += self._generate_passive_mock(task)
        else:
            response = self._generate_passive_mock(task)
        
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
        
        AHORA CON DETECCIÓN Y EJECUCIÓN DE HERRAMIENTAS
        """
        
        task_lower = task.lower()
        
        # DETECTAR SI DEBE USAR POLICY GENERATOR
        policy_keywords = ['genera', 'crea', 'escribe', 'crear', 'generar', 'policy', 'política', 'politica']
        policy_types = {
            'password': 'password_policy',
            'contraseña': 'password_policy',
            'contraseñas': 'password_policy',
            'incidente': 'incident_response',
            'incidentes': 'incident_response',
            'incident': 'incident_response',
            'acceso': 'access_control',
            'access': 'access_control',
            'dato': 'data_classification',
            'datos': 'data_classification',
            'data': 'data_classification',
            'backup': 'backup_recovery',
            'recuperación': 'backup_recovery',
            'recuperacion': 'backup_recovery'
        }
        
        should_generate_policy = any(keyword in task_lower for keyword in policy_keywords)
        detected_policy_type = None
        
        if should_generate_policy:
            for keyword, policy_type in policy_types.items():
                if keyword in task_lower:
                    detected_policy_type = policy_type
                    break
        
        # SI DEBE GENERAR POLÍTICA Y TENEMOS LA TOOL
        if should_generate_policy and detected_policy_type and self.policy_generator:
            
            # Contexto de la empresa
            company_context = {
                'name': context.get('company_name', 'La Organización') if context else 'La Organización',
                'size': context.get('company_size', '20-50') if context else '20-50',
                'industry': context.get('industry', 'Tecnología / SaaS') if context else 'Tecnología / SaaS',
                'tech_stack': context.get('tech_stack', 'Cloud-based') if context else 'Cloud-based',
                'compliance_targets': context.get('compliance_targets', ['SOC 2', 'ISO 27001']) if context else ['SOC 2', 'ISO 27001']
            }
            
            # EJECUTAR LA HERRAMIENTA
            policy_content = self.policy_generator.generate_policy(
                detected_policy_type,
                company_context
            )
            
            policy_info = self.policy_generator.POLICY_TEMPLATES[detected_policy_type]
            
            response = f"""
## ⚡ EJECUTADO CON POLICY GENERATOR

He generado la política solicitada automáticamente.

## 📊 RESULTADO

**Política Generada:** {policy_info['name']}
**Frameworks de Referencia:** {', '.join(policy_info['frameworks'])}
**Controles Aplicables:** {', '.join(policy_info['controls'])}
**Longitud:** ~{len(policy_content.split())} palabras

## 📄 CONTENIDO DE LA POLÍTICA

{policy_content}

## 🧠 MI RAZONAMIENTO

**Por qué ejecuté en MODO DIRECTO:**
1. ✅ Tarea clara: generar una política específica ({detected_policy_type})
2. ✅ Bajo riesgo: solo generación de documentación
3. ✅ No requiere datos sensibles
4. ✅ Resultado predecible y seguro

**Herramienta utilizada:** Policy Generator
**Proceso:** Detecté keywords → Identifiqué tipo de política → Ejecuté generación → Entregué resultado completo

💡 **Nota:** Esta política requiere revisión legal antes de implementación formal.
"""
            
            return {
                "mode": "DIRECT",
                "status": "executed",
                "tool_used": "policy_generator",
                "policy_type": detected_policy_type,
                "policy_content": policy_content,
                "results": response,
                "message": f"⚡ MODO DIRECTO - Ejecutado con Policy Generator\n\n{response}",
                "requires_user_action": False
            }
        
        # SI NO ES GENERACIÓN DE POLÍTICA, FLUJO NORMAL CON LLM
        else:
            if self.use_llm and self.llm:
                prompt = f"""
Eres M.A.R.T.I.N. en MODO DIRECTO - agente autónomo.

Tu trabajo es:
1. Analizar y ejecutar inmediatamente
2. Reportar resultados
3. Explicar tu razonamiento

Tarea: {task}

Responde en este formato:

## ⚡ EJECUTADO
[Qué acciones tomaste]

## 📊 RESULTADOS
[Resultados obtenidos]

## 🧠 MI RAZONAMIENTO
Por qué lo hice así:
- [Razón 1]
- [Razón 2]
"""
                try:
                    response = self.llm.predict(prompt)
                except Exception as e:
                    response = f"Error al llamar LLM: {e}\n"
                    response += self._generate_direct_mock(task)
            else:
                response = self._generate_direct_mock(task)
            
            return {
                "mode": "DIRECT",
                "status": "executed",
                "results": response,
                "message": f"⚡ MODO DIRECTO - Ejecutado automáticamente\n\n{response}",
                "requires_user_action": False
            }
    
    def safe_reasoning(self, task: str, context: Dict = None) -> Dict[str, Any]:
        """
        MODO SEGURO: Genera plan, AUTO-VALIDA, luego decide
        
        Comportamiento:
        1. Analiza la tarea
        2. Genera plan de acción
        3. SE AUTO-CRITICA (validación de riesgos)
        4. Si pasa validación → ejecuta con precauciones
        5. Si NO pasa → sugiere alternativa segura
        """
        
        if self.use_llm and self.llm:
            # Paso 1: Generar plan
            plan_prompt = f"Genera un plan de acción específico para: {task}"
            try:
                plan = self.llm.predict(plan_prompt)
            except:
                plan = f"Plan para: {task}"
            
            # Paso 2: AUTO-VALIDACIÓN
            validation_prompt = f"""
Eres un validador de seguridad crítico.

Tarea: {task}
Plan: {plan}

Analiza riesgos:
1. ¿Es destructivo?
2. ¿Puede causar pérdida de datos?
3. ¿Es reversible?

Responde:

NIVEL DE RIESGO: [BAJO/MEDIO/ALTO/CRÍTICO]

RIESGOS:
- [Riesgo 1]

DECISIÓN: [APROBAR/RECHAZAR]

SI RECHAZAS:
ALTERNATIVA: [alternativa segura]

SI APRUEBAS:
PRECAUCIONES: [lista]
"""
            try:
                validation = self.llm.predict(validation_prompt)
            except:
                validation = self._generate_safe_validation_mock(task)
        else:
            plan = f"Plan para: {task}"
            validation = self._generate_safe_validation_mock(task)
        
        # Analizar resultado
        if "RECHAZAR" in validation or "CRÍTICO" in validation or "ALTO" in validation:
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
            return {
                "mode": "SAFE",
                "status": "approved_and_executed",
                "validation_passed": True,
                "plan": plan,
                "validation_report": validation,
                "message": f"🛡️ MODO SEGURO - Validado y ejecutado\n\n{validation}\n\n✅ EJECUTADO con precauciones.",
                "requires_user_action": False
            }
    
    # Métodos de respuestas simuladas
    
    def _generate_passive_mock(self, task: str) -> str:
        return f"""
## 📋 MI ANÁLISIS
He analizado tu solicitud: "{task}"

## 🎯 PLAN PROPUESTO
1. Analizar requisitos específicos (5 min)
2. Preparar documentación necesaria (15 min)
3. Ejecutar acciones principales (20 min)
4. Verificar resultados (10 min)

## ⚠️ CONSIDERACIONES
- Requiere acceso a ciertos recursos
- Es importante revisar permisos necesarios

¿Procedo con este plan?
"""
    
    def _generate_direct_mock(self, task: str) -> str:
        return f"""
## ⚡ EJECUTADO
He completado la tarea: "{task}"

Acciones realizadas:
- Analicé los requisitos
- Ejecuté el proceso principal
- Validé los resultados

## 📊 RESULTADOS
✅ Tarea completada exitosamente
📁 Documentación generada
🔍 Validación: OK

## 🧠 MI RAZONAMIENTO
Por qué lo hice así:
- La tarea era clara y específica
- No había riesgos de seguridad
- Ejecución directa más eficiente
"""
    
    def _generate_safe_validation_mock(self, task: str) -> str:
        danger_words = ['delete', 'remove', 'destroy', 'disable', 'drop', 'eliminar', 'borrar']
        is_dangerous = any(word in task.lower() for word in danger_words)
        
        if is_dangerous:
            return """
NIVEL DE RIESGO: ALTO

RIESGOS IDENTIFICADOS:
- Acción potencialmente destructiva
- Puede causar pérdida de datos
- Afecta recursos críticos
- Difícil de revertir

DECISIÓN: RECHAZAR

ALTERNATIVA SEGURA:
1. Crear backup completo primero
2. Ejecutar en ambiente de prueba
3. Implementar procedimiento de rollback
4. Obtener aprobación explícita
"""
        else:
            return """
NIVEL DE RIESGO: BAJO

RIESGOS IDENTIFICADOS:
- Riesgo mínimo detectado
- Operación de solo lectura
- No afecta datos críticos

DECISIÓN: APROBAR

PRECAUCIONES:
- Logging habilitado
- Monitoreo activo
- Validación post-ejecución
"""


# Test
if __name__ == "__main__":
    print("🧪 TESTING REASONING ENGINES CON TOOLS\n")
    
    engines = ReasoningEngines(use_llm=False)
    
    print("━━━ TEST 1: PASSIVE ━━━")
    result1 = engines.passive_reasoning("Ayúdame con SOC 2")
    print(result1['message'][:200] + "...")
    print()
    
    print("━━━ TEST 2: DIRECT (sin tool) ━━━")
    result2 = engines.direct_reasoning("Explícame qué es compliance")
    print(result2['message'][:200] + "...")
    print()
    
    print("━━━ TEST 3: DIRECT (CON POLICY GENERATOR) ━━━")
    result3 = engines.direct_reasoning("Genera política de contraseñas")
    print(f"Tool usado: {result3.get('tool_used', 'ninguno')}")
    print(f"Tipo de política: {result3.get('policy_type', 'N/A')}")
    print(f"Longitud de política: {len(result3.get('policy_content', ''))} caracteres")
    print()
    
    print("━━━ TEST 4: SAFE ━━━")
    result4 = engines.safe_reasoning("Delete all users")
    print(result4['message'][:200] + "...")
    print()
    
    print("✅ Tests completados!")