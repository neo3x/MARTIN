"""
ModeSelector - El cerebro que decide cómo M.A.R.T.I.N. debe razonar
"""
from typing import Dict, Literal
import re

ModeType = Literal["PASSIVE", "DIRECT", "SAFE"]

class ModeSelector:
    """
    Analiza la tarea y contexto para determinar el modo de razonamiento óptimo.
    
    Modos:
    - PASSIVE: Tareas ambiguas que requieren clarificación
    - DIRECT: Tareas claras y de bajo riesgo
    - SAFE: Tareas de alto riesgo o en producción
    """
    
    # Palabras clave que indican alto riesgo
    DANGER_KEYWORDS = [
        'delete', 'remove', 'destroy', 'drop', 'disable', 
        'terminate', 'kill', 'shutdown', 'revoke', 'block',
        'eliminar', 'borrar', 'destruir', 'deshabilitar'
    ]
    
    # Palabras que indican ambigüedad o necesidad de clarificación
    VAGUE_KEYWORDS = [
        'ayuda', 'ayúdame', 'help', 'cómo', 'qué debo', 'no sé',
        'podrías', 'puedes', 'quiero', 'necesito'
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
            reason = f"Riesgo alto detectado (score: {risk_score:.2f})"
        
        # 3. Baja claridad va a PASSIVE
        elif clarity_score < 0.5:
            mode = "PASSIVE"
            reason = f"Tarea ambigua o requiere clarificación (clarity: {clarity_score:.2f})"
        
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
        mode_emoji = {
            "PASSIVE": "🟦",
            "DIRECT": "🟩",
            "SAFE": "🟨"
        }
        
        emoji = mode_emoji.get(last['selected_mode'], "⚪")
        
        return f"""
{emoji} Decisión del ModeSelector:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tarea: "{last['task']}"
Modo seleccionado: {last['selected_mode']}
Razón: {last['reason']}

Factores analizados:
  • Riesgo: {last['risk_score']:.2f} (0=seguro, 1=peligroso)
  • Claridad: {last['clarity_score']:.2f} (0=vago, 1=claro)
  • Ambiente: {last['environment']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# Test rápido
if __name__ == "__main__":
    selector = ModeSelector()
    
    test_cases = [
        ("Ayúdame con SOC 2", {}),
        ("Genera política de contraseñas para ISO 27001", {}),
        ("Delete all users from database", {}),
        ("Actualiza configuración", {'environment': 'production'}),
        ("¿Cómo configuro mi firewall?", {})
    ]
    
    print("🧪 TESTING MODE SELECTOR\n")
    
    for task, context in test_cases:
        mode = selector.select_mode(task, context)
        print(f"Input: \"{task}\"")
        print(f"Context: {context}")
        print(f"→ Modo: {mode}")
        print(selector.explain_last_decision())
        print("\n")