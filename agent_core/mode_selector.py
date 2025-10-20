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
        'terminate', 'kill', 'shutdown', 'revoke', 'block',
        'eliminar', 'borrar', 'destruir', 'deshabilitar',
        'terminar', 'apagar', 'revocar', 'bloquear'
    ]
    
    # Palabras que indican ambigüedad o necesidad de clarificación
    VAGUE_KEYWORDS = [
        'ayuda', 'ayúdame', 'help', 'cómo', 'qué debo', 'no sé',
        'explicame', 'explícame', 'necesito', 'quiero', 'puedo',
        'debería', 'podría', 'tal vez', 'quizás'
    ]
    
    # Recursos críticos que aumentan el riesgo
    CRITICAL_RESOURCES = [
        'database', 'db', 'producción', 'production', 
        'payment', 'billing', 'auth', 'users', 'admin',
        'password', 'credentials', 'secret', 'token',
        'base de datos', 'pago', 'facturación', 'usuarios'
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
        
        # 4. Riesgo medio con claridad media va a PASSIVE
        elif risk_score >= 0.4 and clarity_score < 0.7:
            mode = "PASSIVE"
            reason = "Combinación de riesgo moderado y claridad insuficiente"
        
        # 5. Clara y segura va a DIRECT
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
        - Contexto del ambiente
        """
        risk = 0.0
        task_lower = task.lower()
        
        # Factor 1: Palabras peligrosas (40% del peso)
        danger_words_found = sum(1 for word in self.DANGER_KEYWORDS if word in task_lower)
        if danger_words_found > 0:
            risk += 0.4 * min(danger_words_found / 2, 1.0)
        
        # Factor 2: Recursos críticos (30% del peso)
        critical_resources_found = sum(1 for resource in self.CRITICAL_RESOURCES 
                                      if resource in task_lower)
        if critical_resources_found > 0:
            risk += 0.3 * min(critical_resources_found / 2, 1.0)
        
        # Factor 3: Scope amplio (20% del peso)
        broad_scope_indicators = ['all', 'every', 'todos', 'cada', 'entire', 
                                 'completo', 'total', '*', 'cualquier']
        if any(indicator in task_lower for indicator in broad_scope_indicators):
            risk += 0.2
        
        # Factor 4: Contexto de ambiente (10% del peso)
        if context.get('has_active_users', False):
            risk += 0.1
        
        # Factor 5: Operaciones irreversibles
        irreversible_keywords = ['permanent', 'permanente', 'forever', 
                               'siempre', 'definitivo', 'final']
        if any(keyword in task_lower for keyword in irreversible_keywords):
            risk += 0.2
        
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
        
        # Factor 1: Es una pregunta (reduce claridad 30%)
        if '?' in task or task_lower.startswith(('qué', 'cómo', 'cuándo', 
                                                'dónde', 'por qué', 'what', 
                                                'how', 'when', 'where', 'why')):
            clarity -= 0.3
        
        # Factor 2: Palabras vagas (reduce 15% por cada una)
        vague_words_found = sum(1 for word in self.VAGUE_KEYWORDS 
                               if word in task_lower.split())
        clarity -= min(0.15 * vague_words_found, 0.45)
        
        # Factor 3: Longitud (muy corto = vago)
        word_count = len(task.split())
        if word_count < 3:
            clarity -= 0.5
        elif word_count < 5:
            clarity -= 0.3
        elif word_count > 15:  # Instrucciones muy largas son claras
            clarity += 0.1
        
        # Factor 4: Contiene entidades específicas (aumenta claridad)
        # Buscar nombres propios, números, rutas, etc.
        has_specifics = bool(re.search(r'[A-Z][a-z]+|/[\w/]+|\d+|\w+@\w+\.\w+', task))
        if has_specifics:
            clarity += 0.2
        
        # Factor 5: Tiene verbos de acción claros
        action_verbs = ['genera', 'crea', 'analiza', 'evalúa', 'escanea', 
                       'revisa', 'audita', 'compara', 'generate', 'create', 
                       'analyze', 'evaluate', 'scan', 'review', 'audit']
        if any(verb in task_lower for verb in action_verbs):
            clarity += 0.15
        
        return max(min(clarity, 1.0), 0.0)
    
    def explain_last_decision(self) -> str:
        """Retorna explicación de la última decisión tomada"""
        if not self.decision_log:
            return "No hay decisiones registradas aún"
        
        last = self.decision_log[-1]
        
        # Determinar emoji según modo
        mode_emoji = {
            'PASSIVE': '🟦',
            'DIRECT': '🟩',
            'SAFE': '🟨'
        }
        
        return f"""
Decisión del ModeSelector:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tarea: "{last['task']}"
Modo seleccionado: {mode_emoji.get(last['selected_mode'], '⚪')} {last['selected_mode']}
Razón: {last['reason']}

Factores analizados:
  • Riesgo: {last['risk_score']:.2f}/1.00 (0=seguro, 1=peligroso)
  • Claridad: {last['clarity_score']:.2f}/1.00 (0=vago, 1=claro)
  • Ambiente: {last['environment']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    def get_statistics(self) -> Dict:
        """Retorna estadísticas de todas las decisiones tomadas"""
        if not self.decision_log:
            return {"message": "No hay estadísticas disponibles aún"}
        
        total = len(self.decision_log)
        modes_count = {
            'PASSIVE': sum(1 for d in self.decision_log if d['selected_mode'] == 'PASSIVE'),
            'DIRECT': sum(1 for d in self.decision_log if d['selected_mode'] == 'DIRECT'),
            'SAFE': sum(1 for d in self.decision_log if d['selected_mode'] == 'SAFE')
        }
        
        avg_risk = sum(d['risk_score'] for d in self.decision_log) / total
        avg_clarity = sum(d['clarity_score'] for d in self.decision_log) / total
        
        return {
            'total_decisions': total,
            'modes_distribution': modes_count,
            'average_risk_score': round(avg_risk, 2),
            'average_clarity_score': round(avg_clarity, 2),
            'most_used_mode': max(modes_count, key=modes_count.get)
        }