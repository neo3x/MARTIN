"""
Los 3 motores de razonamiento de M.A.R.T.I.N.
"""
from typing import Dict, Any
import os

class ReasoningEngines:
    """
    Contiene los 3 modos de razonamiento de M.A.R.T.I.N.
    """
    
    def __init__(self, use_llm: bool = False):
        """
        Args:
            use_llm: Si True, usa LLM real. Si False, genera respuestas simuladas.
        """
        self.use_llm = use_llm
        self.llm = None
        
        if self.use_llm:
            try:
                from langchain.chat_models import ChatOpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key:
                    self.llm = ChatOpenAI(
                        model="gpt-4",
                        temperature=0,
                        api_key=api_key
                    )
                else:
                    print("⚠️ OPENAI_API_KEY no configurada. Usando modo simulado.")
                    self.use_llm = False
            except ImportError:
                print("⚠️ langchain no instalado. Usando modo simulado.")
                self.use_llm = False
    
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
            # Usar LLM real
            prompt = f"""
Eres M.A.R.T.I.N., un agente de IA en MODO PASIVO.

En este modo eres consultivo y colaborativo. Tu objetivo es:
1. Entender profundamente lo que el usuario necesita
2. Proponer un plan de acción detallado
3. Explicar las opciones disponibles
4. ESPERAR confirmación antes de proceder

Tarea del usuario: {task}
Contexto: {context if context else "No hay contexto adicional"}

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

## 🤔 PREGUNTAS PARA TI
1. [Pregunta para clarificar]

¿Te parece bien este plan? ¿Quieres que ajuste algo antes de empezar?
"""
            try:
                response = self.llm.predict(prompt)
            except Exception as e:
                response = f"Error al llamar LLM: {e}\nUsando respuesta simulada."
                response += self._generate_simulated_passive_response(task)
        else:
            # Usar respuesta simulada
            response = self._generate_simulated_passive_response(task)
        
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
        
        if self.use_llm and self.llm:
            prompt = f"""
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

Por qué lo hice así:
- [Razón 1]
- [Razón 2]
"""
            try:
                response = self.llm.predict(prompt)
            except Exception as e:
                response = f"Error al llamar LLM: {e}\nUsando respuesta simulada."
                response += self._generate_simulated_direct_response(task)
        else:
            response = self._generate_simulated_direct_response(task)
        
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
        5. Si NO pasa → sugiere alternativa segura
        """
        
        if self.use_llm and self.llm:
            # Paso 1: Generar plan
            plan_prompt = f"Genera un plan de acción específico para: {task}"
            try:
                plan = self.llm.predict(plan_prompt)
            except:
                plan = f"Plan para: {task}"
            
            # Paso 2: AUTO-VALIDACIÓN (CRÍTICO)
            validation_prompt = f"""
Eres un validador de seguridad crítico.

Tarea original: {task}
Plan propuesto: {plan}

Analiza riesgos:
1. ¿Es destructivo?
2. ¿Puede causar pérdida de datos?
3. ¿Afecta sistemas críticos?
4. ¿Es reversible?

Responde:

NIVEL DE RIESGO: [BAJO/MEDIO/ALTO/CRÍTICO]

RIESGOS IDENTIFICADOS:
- [Riesgo 1]

DECISIÓN: [APROBAR/RECHAZAR]

SI RECHAZAS:
ALTERNATIVA SEGURA: [descripción]

SI APRUEBAS:
PRECAUCIONES: [lista]
"""
            try:
                validation = self.llm.predict(validation_prompt)
            except:
                validation = self._generate_simulated_safe_validation(task)
        else:
            plan = f"Plan para: {task}"
            validation = self._generate_simulated_safe_validation(task)
        
        # Analizar resultado de validación
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
                "results": "[Simulación de ejecución segura]",
                "message": f"🛡️ MODO SEGURO - Validado y ejecutado\n\n{validation}\n\n✅ EJECUTADO con precauciones.",
                "requires_user_action": False
            }
    
    # Métodos de respuestas simuladas
    
    def _generate_simulated_passive_response(self, task: str) -> str:
        return f"""
## 📋 MI ANÁLISIS
He analizado tu solicitud: "{task}"

Parece que necesitas ayuda con una tarea que requiere varios pasos y decisiones.

## 🎯 PLAN PROPUESTO

Paso 1: Analizar los requisitos específicos (5 minutos)
Paso 2: Preparar la documentación necesaria (15 minutos)
Paso 3: Ejecutar las acciones principales (20 minutos)
Paso 4: Verificar y validar resultados (10 minutos)

## ⚠️ CONSIDERACIONES IMPORTANTES
- Esta tarea requiere acceso a ciertos recursos
- Es importante revisar los permisos necesarios
- Debemos asegurar que no haya conflictos

## 🤔 PREGUNTAS PARA TI
1. ¿Hay alguna restricción de tiempo?
2. ¿Tienes acceso a todos los recursos necesarios?

¿Te parece bien este plan? ¿Quieres que ajuste algo antes de empezar?
"""
    
    def _generate_simulated_direct_response(self, task: str) -> str:
        return f"""
## ⚡ EJECUTADO
He completado la tarea: "{task}"

Acciones realizadas:
- Analicé los requisitos
- Preparé los recursos necesarios
- Ejecuté el proceso principal
- Validé los resultados

## 📊 RESULTADOS
✅ Tarea completada exitosamente
📁 Documentación generada
🔍 Validación: OK

## 🧠 MI RAZONAMIENTO

Pasos que seguí:
1. Identificación rápida de la tarea clara y directa
2. Ejecución inmediata sin necesidad de clarificación
3. Validación automática de resultados

Por qué lo hice así:
- La tarea era clara y específica
- No había riesgos de seguridad significativos
- La ejecución directa es más eficiente en este caso
"""
    
    def _generate_simulated_safe_validation(self, task: str) -> str:
        # Detectar si es peligroso
        danger_words = ['delete', 'remove', 'destroy', 'disable', 'drop', 'eliminar', 'borrar']
        is_dangerous = any(word in task.lower() for word in danger_words)
        
        if is_dangerous:
            return f"""
NIVEL DE RIESGO: ALTO

RIESGOS IDENTIFICADOS:
- Acción potencialmente destructiva detectada
- Puede causar pérdida de datos o acceso
- Afecta recursos críticos del sistema
- Difícil o imposible de revertir

DECISIÓN: RECHAZAR

ALTERNATIVA SEGURA:
En lugar de ejecutar esta acción directamente, sugiero:
1. Crear un backup completo primero
2. Ejecutar en ambiente de prueba
3. Implementar un procedimiento de rollback
4. Obtener aprobación explícita de supervisores

Esta alternativa protege contra errores costosos y mantiene la integridad del sistema.
"""
        else:
            return f"""
NIVEL DE RIESGO: BAJO

RIESGOS IDENTIFICADOS:
- Riesgo mínimo detectado
- Operación parece ser de solo lectura o baja criticidad
- No afecta datos críticos

DECISIÓN: APROBAR

PRECAUCIONES NECESARIAS:
- Logging habilitado para auditoría
- Monitoreo de la operación
- Validación de resultados post-ejecución

Procedo con la ejecución de forma segura.
"""