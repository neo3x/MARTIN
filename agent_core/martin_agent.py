"""
M.A.R.T.I.N. Agent - Integración completa del sistema
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, Optional, List
from datetime import datetime
from agent_core.mode_selector import ModeSelector
from agent_core.reasoning_engines import ReasoningEngines

class MARTINAgent:
    """
    Agente principal que orquesta:
    1. Selección de modo
    2. Razonamiento apropiado
    3. Ejecución (si corresponde)
    4. Gestión del historial de conversación
    """
    
    def __init__(self, use_llm: bool = False, verbose: bool = True):
        """
        Args:
            use_llm: Si True, usa LLM real. Si False, usa respuestas simuladas.
            verbose: Si True, imprime información de debug.
        """
        self.mode_selector = ModeSelector()
        self.reasoning = ReasoningEngines(use_llm=use_llm)
        self.conversation_history = []
        self.verbose = verbose
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if self.verbose:
            print(f"🧠 M.A.R.T.I.N. Agent iniciado")
            print(f"   Session ID: {self.session_id}")
            print(f"   Modo LLM: {'Activado' if use_llm else 'Simulado'}")
            print("="*50)
    
    def process(self, user_input: str, context: Dict = None) -> Dict[str, Any]:
        """
        Procesa input del usuario a través de M.A.R.T.I.N.
        
        Flujo:
        1. Selecciona modo apropiado
        2. Aplica razonamiento según modo
        3. Retorna respuesta estructurada
        
        Args:
            user_input: Instrucción o consulta del usuario
            context: Contexto adicional (environment, user_role, etc.)
        
        Returns:
            Dict con la respuesta estructurada del agente
        """
        if context is None:
            context = {}
        
        # Log de entrada
        if self.verbose:
            print(f"\n📥 INPUT: {user_input[:100]}...")
            if context:
                print(f"📌 Contexto: {context}")
        
        # Paso 1: Decidir modo
        selected_mode = self.mode_selector.select_mode(user_input, context)
        
        if self.verbose:
            mode_emoji = {'PASSIVE': '🟦', 'DIRECT': '🟩', 'SAFE': '🟨'}
            print(f"🎯 Modo seleccionado: {mode_emoji.get(selected_mode, '⚪')} {selected_mode}")
        
        # Paso 2: Aplicar razonamiento según modo
        if selected_mode == "PASSIVE":
            result = self.reasoning.passive_reasoning(user_input, context)
        elif selected_mode == "DIRECT":
            result = self.reasoning.direct_reasoning(user_input, context)
        else:  # SAFE
            result = self.reasoning.safe_reasoning(user_input, context)
        
        # Agregar metadatos
        result['input'] = user_input
        result['mode_explanation'] = self.mode_selector.explain_last_decision()
        result['session_id'] = self.session_id
        result['interaction_id'] = len(self.conversation_history)
        
        # Guardar en historial
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'input': user_input,
            'context': context,
            'mode_selected': selected_mode,
            'result': result
        })
        
        if self.verbose:
            print(f"📤 Respuesta generada ({result.get('status', 'unknown')})")
            if result.get('requires_user_action'):
                print("⏳ Esperando acción del usuario...")
        
        return result
    
    def confirm_action(self, interaction_id: int, confirmed: bool = True) -> Dict[str, Any]:
        """
        Confirma o rechaza una acción pendiente (para modo PASSIVE o SAFE bloqueado)
        
        Args:
            interaction_id: ID de la interacción a confirmar
            confirmed: True para proceder, False para cancelar
        
        Returns:
            Dict con el resultado de la confirmación
        """
        if interaction_id >= len(self.conversation_history):
            return {
                'error': 'ID de interacción inválido',
                'message': f'No existe interacción con ID {interaction_id}'
            }
        
        interaction = self.conversation_history[interaction_id]
        
        if not interaction['result'].get('requires_user_action'):
            return {
                'error': 'No requiere confirmación',
                'message': 'Esta interacción no está esperando confirmación'
            }
        
        if confirmed:
            # Usuario confirmó - proceder con la ejecución
            if self.verbose:
                print(f"✅ Usuario confirmó acción para interacción {interaction_id}")
            
            # Cambiar a modo DIRECT para ejecutar
            original_input = interaction['input']
            original_context = interaction['context']
            original_context['user_confirmed'] = True
            
            # Re-procesar en modo DIRECT (ya fue aprobado por usuario)
            execution_result = self.reasoning.direct_reasoning(original_input, original_context)
            execution_result['confirmed_by_user'] = True
            execution_result['original_mode'] = interaction['mode_selected']
            
            # Actualizar historial
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'confirmation',
                'confirmed': True,
                'interaction_id': interaction_id,
                'result': execution_result
            })
            
            return execution_result
        else:
            # Usuario rechazó - cancelar
            if self.verbose:
                print(f"❌ Usuario rechazó acción para interacción {interaction_id}")
            
            cancellation_result = {
                'status': 'cancelled',
                'message': '❌ Acción cancelada por el usuario',
                'interaction_id': interaction_id,
                'timestamp': datetime.now().isoformat()
            }
            
            # Actualizar historial
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'confirmation',
                'confirmed': False,
                'interaction_id': interaction_id,
                'result': cancellation_result
            })
            
            return cancellation_result
    
    def get_conversation_history(self) -> List[Dict]:
        """Retorna historial completo de la conversación"""
        return self.conversation_history
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Retorna resumen de la sesión actual"""
        total_interactions = len([h for h in self.conversation_history if h.get('input')])
        confirmations = len([h for h in self.conversation_history if h.get('type') == 'confirmation'])
        
        modes_used = {}
        for h in self.conversation_history:
            if 'mode_selected' in h:
                mode = h['mode_selected']
                modes_used[mode] = modes_used.get(mode, 0) + 1
        
        return {
            'session_id': self.session_id,
            'total_interactions': total_interactions,
            'total_confirmations': confirmations,
            'modes_distribution': modes_used,
            'start_time': self.conversation_history[0]['timestamp'] if self.conversation_history else None,
            'last_activity': self.conversation_history[-1]['timestamp'] if self.conversation_history else None
        }
    
    def reset(self):
        """Reinicia el agente (nueva sesión)"""
        self.conversation_history = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.mode_selector = ModeSelector()
        
        if self.verbose:
            print(f"\n🔄 Agente reiniciado - Nueva sesión: {self.session_id}")
    
    def export_conversation(self, format: str = 'json') -> Any:
        """
        Exporta la conversación en el formato especificado
        
        Args:
            format: 'json', 'text', o 'markdown'
        
        Returns:
            Conversación en el formato solicitado
        """
        if format == 'json':
            import json
            return json.dumps(self.conversation_history, indent=2, default=str)
        
        elif format == 'text':
            output = f"M.A.R.T.I.N. Session: {self.session_id}\n"
            output += "="*50 + "\n\n"
            
            for item in self.conversation_history:
                if item.get('input'):
                    output += f"[{item['timestamp']}]\n"
                    output += f"Usuario: {item['input']}\n"
                    output += f"Modo: {item['mode_selected']}\n"
                    output += f"M.A.R.T.I.N.: {item['result'].get('message', 'Sin respuesta')}\n"
                    output += "-"*30 + "\n\n"
            
            return output
        
        elif format == 'markdown':
            output = f"# M.A.R.T.I.N. Session Report\n\n"
            output += f"**Session ID:** {self.session_id}\n\n"
            output += f"## Conversación\n\n"
            
            for item in self.conversation_history:
                if item.get('input'):
                    mode_emoji = {
                        'PASSIVE': '🟦',
                        'DIRECT': '🟩',
                        'SAFE': '🟨'
                    }.get(item['mode_selected'], '⚪')
                    
                    output += f"### {item['timestamp']}\n\n"
                    output += f"**Usuario:** {item['input']}\n\n"
                    output += f"**Modo:** {mode_emoji} {item['mode_selected']}\n\n"
                    output += f"**M.A.R.T.I.N.:**\n{item['result'].get('message', 'Sin respuesta')}\n\n"
                    output += "---\n\n"
            
            return output
        
        else:
            raise ValueError(f"Formato no soportado: {format}")