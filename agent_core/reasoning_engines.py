"""
Los 3 motores de razonamiento de M.A.R.T.I.N.
"""
from typing import Dict, Any, Optional
import os
from datetime import datetime

# Por ahora usamos respuestas simuladas para no depender de APIs externas
# En producción, descomentar las importaciones de LangChain/OpenAI

class ReasoningEngines:
    """
    Contiene los 3 modos de razonamiento de M.A.R.T.I.N.
    Cada modo tiene un comportamiento diferente según el contexto.
    """
    
    def __init__(self, use_llm: bool = False):
        """
        Args:
            use_llm: Si True, usa LLM real. Si False, usa respuestas simuladas.
        """
        self.use_llm = use_llm
        
        if use_llm:
            try:
                from langchain.chat_models import ChatOpenAI
                self.llm = ChatOpenAI(
                    model="gpt-4",
                    temperature=0,
                    api_key=os.getenv("OPENAI_API_KEY")
                )
            except ImportError:
                print("⚠️ LangChain no instalado. Usando modo simulado.")
                self.use_llm = False
                self.llm = None
        else:
            self.llm = None
    
    def passive_reasoning(self, task: str, context: Dict = None) -> Dict[str, Any]:
        """
        MODO PASIVO: Genera plan pero NO ejecuta
        
        Comportamiento:
        1. Analiza la tarea del usuario
        2. Genera un plan detallado
        3. Explica qué hará
        4. ESPERA confirmación del usuario
        """
        
        if context is None:
            context = {}
        
        if self.use_llm and self.llm:
            # Usar LLM real
            from langchain.prompts import PromptTemplate
            
            prompt = PromptTemplate(
                input_variables=["task", "context"],
                template=self._get_passive_prompt_template()
            )
            
            response = self.llm.predict(
                prompt.format(
                    task=task,
                    context=str(context) if context else "No hay contexto adicional"
                )
            )
        else:
            # Respuesta simulada para testing
            response = self._generate_passive_response_mock(task, context)
        
        return {
            "mode": "PASSIVE",
            "status": "awaiting_confirmation",
            "plan": response,
            "message": f"📋 MODO PASIVO ACTIVADO\n\n{response}",
            "requires_user_action": True,
            "timestamp": datetime.now().isoformat()
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
        
        if context is None:
            context = {}
        
        if self.use_llm and self.llm:
            # Usar LLM real
            from langchain.prompts import PromptTemplate
            
            prompt = PromptTemplate(
                input_variables=["task"],
                template=self._get_direct_prompt_template()
            )
            
            response = self.llm.predict(prompt.format(task=task))
        else:
            # Respuesta simulada para testing
            response = self._generate_direct_response_mock(task, context)
        
        return {
            "mode": "DIRECT",
            "status": "executed",
            "results": response,
            "message": f"⚡ MODO DIRECTO - Ejecutado automáticamente\n\n{response}",
            "requires_user_action": False,
            "reasoning_visible": True,
            "timestamp": datetime.now().isoformat()
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
        
        if context is None:
            context = {}
        
        # Generar plan inicial
        plan = self._generate_initial_plan(task, context)
        
        # Auto-validación del plan
        validation_result = self._validate_plan_safety(task, plan, context)
        
        # Decidir basado en validación
        if validation_result['is_safe']:
            # Plan aprobado - ejecutar con precauciones
            return {
                "mode": "SAFE",
                "status": "approved_and_executed",
                "validation_passed": True,
                "plan": plan,
                "validation_report": validation_result['report'],
                "precautions": validation_result['precautions'],
                "results": f"[Ejecutado con precauciones: {', '.join(validation_result['precautions'])}]",
                "message": f"🛡️ MODO SEGURO - Validado y ejecutado\n\n{validation_result['report']}",
                "requires_user_action": False,
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Plan rechazado - bloquear y sugerir alternativa
            return {
                "mode": "SAFE",
                "status": "blocked",
                "validation_failed": True,
                "original_plan": plan,
                "validation_report": validation_result['report'],
                "risks_identified": validation_result['risks'],
                "alternative_suggestion": validation_result['alternative'],
                "message": f"🛡️ MODO SEGURO - ACCIÓN BLOQUEADA\n\n{validation_result['report']}",
                "requires_user_action": True,
                "timestamp": datetime.now().isoformat()
            }
    
    # ========== Métodos auxiliares ==========
    
    def _get_passive_prompt_template(self) -> str:
        """Retorna el template del prompt para modo pasivo"""
        return """
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
    
    def _get_direct_prompt_template(self) -> str:
        """Retorna el template del prompt para modo directo"""
        return """
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
"""
    
    def _generate_passive_response_mock(self, task: str, context: Dict) -> str:
        """Genera respuesta simulada para modo pasivo"""
        return f"""
## 📋 MI ANÁLISIS
He analizado tu solicitud: "{task[:100]}..." 
Entiendo que necesitas ayuda con tareas de compliance y preparación para certificación.

## 🎯 PLAN PROPUESTO

**Fase 1: Evaluación inicial** (2 horas)
- Paso 1: Auditar tu infraestructura actual (45 min)
- Paso 2: Identificar gaps críticos de compliance (45 min)
- Paso 3: Priorizar por impacto y urgencia (30 min)

**Fase 2: Implementación** (2 semanas)
- Paso 4: Generar políticas faltantes (3 días)
- Paso 5: Implementar controles técnicos (1 semana)
- Paso 6: Documentar procedimientos (4 días)

**Fase 3: Validación** (1 semana)
- Paso 7: Recopilar evidencia (3 días)
- Paso 8: Pre-auditoría interna (2 días)
- Paso 9: Correcciones finales (2 días)

## ⚠️ CONSIDERACIONES IMPORTANTES
- Este plan asume una organización de 20-50 empleados
- Requiere dedicación del equipo técnico (~4h/semana)
- Los tiempos pueden variar según la complejidad actual
- Recomiendo empezar por los gaps críticos primero

## 🤔 PREGUNTAS PARA TI
1. ¿Cuál es el tamaño actual de tu organización?
2. ¿Tienes alguna fecha límite para la certificación?
3. ¿Prefieres empezar con SOC 2 o ISO 27001?

¿Te parece bien este plan? ¿Quieres que ajuste algo antes de empezar?"""
    
    def _generate_direct_response_mock(self, task: str, context: Dict) -> str:
        """Genera respuesta simulada para modo directo"""
        return f"""
## ⚡ EJECUTADO
He ejecutado automáticamente las siguientes acciones:
1. Analizado los requisitos de "{task[:50]}..."
2. Generado la documentación solicitada
3. Aplicado mejores prácticas de la industria

## 📊 RESULTADOS

**Política generada:** Política de Contraseñas según ISO 27001

### Requisitos mínimos:
- Longitud: 12 caracteres mínimo
- Complejidad: Mayúsculas, minúsculas, números y símbolos
- Rotación: Cada 90 días
- Historia: No reusar últimas 12 contraseñas
- MFA: Obligatorio para cuentas administrativas

### Implementación:
- Aplicar en Active Directory/LDAP
- Configurar en aplicaciones cloud
- Documentar excepciones autorizadas

### Medición y cumplimiento:
- Auditorías trimestrales
- Reporte mensual de cumplimiento
- Capacitación anual obligatoria

## 🧠 MI RAZONAMIENTO
Tomé estas decisiones porque:
1. ISO 27001 requiere controles específicos de acceso (A.9.4.3)
2. 12 caracteres es el mínimo actual recomendado por NIST
3. MFA es crítico para cuentas privilegiadas
4. La rotación de 90 días balancea seguridad y usabilidad

Esta política cumple con los estándares y es práctica para implementar."""
    
    def _generate_initial_plan(self, task: str, context: Dict) -> str:
        """Genera un plan inicial para validación"""
        return f"""
Plan de acción para: {task}
1. Identificar recursos afectados
2. Evaluar impacto de la operación
3. Ejecutar cambios solicitados
4. Verificar resultados
5. Documentar acciones tomadas"""
    
    def _validate_plan_safety(self, task: str, plan: str, context: Dict) -> Dict[str, Any]:
        """
        Valida la seguridad del plan (auto-crítica)
        Retorna diccionario con resultado de validación
        """
        task_lower = task.lower()
        
        # Lista de indicadores de alto riesgo
        high_risk_indicators = [
            'delete', 'remove', 'destroy', 'disable', 'drop',
            'eliminar', 'borrar', 'deshabilitar', 'destruir'
        ]
        
        critical_resources = [
            'admin', 'production', 'database', 'payment', 'auth',
            'password', 'credential', 'secret', 'mfa', '2fa'
        ]
        
        # Detectar riesgos
        risks = []
        risk_level = "BAJO"
        
        for indicator in high_risk_indicators:
            if indicator in task_lower:
                risks.append(f"Operación destructiva detectada: '{indicator}'")
                risk_level = "ALTO"
        
        for resource in critical_resources:
            if resource in task_lower:
                risks.append(f"Recurso crítico afectado: '{resource}'")
                if risk_level != "ALTO":
                    risk_level = "MEDIO"
        
        # Si es producción, aumentar nivel de riesgo
        if context.get('environment') == 'production':
            risks.append("Operación en ambiente de PRODUCCIÓN")
            risk_level = "CRÍTICO"
        
        # Determinar si es seguro proceder
        is_safe = risk_level in ["BAJO", "MEDIO"]
        
        if is_safe:
            # Plan aprobado con precauciones
            precautions = []
            if risk_level == "MEDIO":
                precautions = [
                    "Crear backup antes de proceder",
                    "Ejecutar en horario de bajo impacto",
                    "Tener plan de rollback preparado"
                ]
            else:
                precautions = ["Monitorear resultados", "Documentar cambios"]
            
            report = f"""
## 🔍 ANÁLISIS DE SEGURIDAD COMPLETADO

**Nivel de riesgo:** {risk_level}
**Decisión:** ✅ APROBADO PARA EJECUCIÓN

### Plan validado:
{plan}

### Precauciones a aplicar:
{chr(10).join(f'- {p}' for p in precautions)}

### Factores evaluados:
- Reversibilidad: SÍ
- Impacto en usuarios: MÍNIMO
- Riesgo de pérdida de datos: BAJO

Procedo con la ejecución aplicando las precauciones listadas."""
            
            return {
                'is_safe': True,
                'risk_level': risk_level,
                'risks': risks,
                'precautions': precautions,
                'report': report,
                'alternative': None
            }
        else:
            # Plan rechazado - muy riesgoso
            alternative = self._generate_safe_alternative(task)
            
            report = f"""
## 🔍 ANÁLISIS DE SEGURIDAD - CRÍTICO

**Nivel de riesgo:** ⚠️ {risk_level}
**Decisión:** ❌ ACCIÓN BLOQUEADA

### Riesgos identificados:
{chr(10).join(f'- {r}' for r in risks)}

### Plan original (RECHAZADO):
{plan}

### Por qué fue bloqueado:
1. La acción podría causar pérdida de datos o acceso
2. Impacto potencial en sistemas críticos
3. Dificultad o imposibilidad de reversión
4. Violación potencial de políticas de seguridad

### 🔄 ALTERNATIVA SEGURA SUGERIDA:
{alternative}

### Recomendación:
Revisa la alternativa propuesta o consulta con el equipo de seguridad antes de proceder.

¿Deseas proceder con la alternativa segura propuesta?"""
            
            return {
                'is_safe': False,
                'risk_level': risk_level,
                'risks': risks,
                'precautions': [],
                'report': report,
                'alternative': alternative
            }
    
    def _generate_safe_alternative(self, task: str) -> str:
        """Genera una alternativa más segura para una tarea riesgosa"""
        task_lower = task.lower()
        
        if 'deshabilitar' in task_lower or 'disable' in task_lower:
            if 'mfa' in task_lower or '2fa' in task_lower or 'admin' in task_lower:
                return """
1. En lugar de deshabilitar MFA completamente:
   - Genera códigos de respaldo temporales
   - Configura un método alternativo de MFA (SMS, app authenticator)
   - Crea una cuenta administrativa temporal con permisos limitados
   
2. Si el usuario está bloqueado:
   - Resetea el MFA manteniendo la protección activa
   - Usa el proceso de recuperación estándar
   - Contacta al usuario para verificación de identidad"""
        
        elif 'delete' in task_lower or 'eliminar' in task_lower or 'borrar' in task_lower:
            return """
1. En lugar de eliminar permanentemente:
   - Archivar los recursos en lugar de eliminarlos
   - Hacer un backup completo antes de cualquier eliminación
   - Marcar para eliminación y aplicar después de período de gracia
   
2. Para limpieza segura:
   - Eliminar en ambiente de desarrollo primero
   - Validar con el equipo antes de proceder
   - Documentar razón y obtener aprobación escrita"""
        
        else:
            return """
1. Enfoque más seguro:
   - Ejecutar primero en ambiente de desarrollo/staging
   - Implementar cambios gradualmente
   - Crear punto de restauración antes de proceder
   
2. Validación adicional:
   - Revisar con el equipo de seguridad
   - Documentar el cambio en el sistema de tickets
   - Programar ventana de mantenimiento si es necesario"""