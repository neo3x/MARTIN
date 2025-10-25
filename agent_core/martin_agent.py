"""
M.A.R.T.I.N. Agent - Integración completa con sistema de confirmación mejorado
"""
import sys
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import re

# Importar componentes core
from agent_core.mode_selector import ModeSelector
from agent_core.reasoning_engines import ReasoningEngines

class MARTINAgent:
    """
    Agente principal que orquesta:
    1. Selección de modo
    2. Razonamiento apropiado
    3. Ejecución (si corresponde)
    4. Gestión del historial de conversación
    5. Sistema de confirmación de acciones
    
    Soporta OpenAI (GPT-4) y Anthropic (Claude)
    """
    
    def __init__(self, use_llm: bool = False, llm_provider: str = "auto", verbose: bool = True):
        """
        Args:
            use_llm: Si True, usa LLM real. Si False, usa respuestas simuladas.
            llm_provider: "openai", "claude", o "auto" (detecta automáticamente)
            verbose: Si True, imprime información de debug.
        """
        self.mode_selector = ModeSelector()
        self.reasoning = ReasoningEngines(use_llm=use_llm, llm_provider=llm_provider)
        self.conversation_history = []
        self.verbose = verbose
        self.use_llm = use_llm
        self.llm_provider = self.reasoning.llm_provider
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Estado para manejo de confirmaciones
        self.pending_action: Optional[Dict] = None
        
        if self.verbose:
            print(f"🧠 M.A.R.T.I.N. Agent iniciado")
            print(f"   Session ID: {self.session_id}")
            if use_llm and self.llm_provider:
                provider_name = {
                    "openai": "OpenAI GPT-4",
                    "claude": "Anthropic Claude 3.5 Sonnet"
                }.get(self.llm_provider, "Desconocido")
                print(f"   LLM: {provider_name} ✓")
            else:
                print(f"   Modo: Simulado (sin API key)")
            print("="*50)
    
    def _is_confirmation(self, text: str) -> bool:
        """
        Detecta si el texto del usuario es una confirmación
        
        Args:
            text: Texto del usuario
            
        Returns:
            True si es una confirmación, False si no
        """
        text_lower = text.lower().strip()
        
        # Palabras de confirmación en español e inglés
        confirmations = [
            # Español
            'sí', 'si', 's', 'ok', 'okay', 'vale', 'confirmar', 'confirmo',
            'proceder', 'procede', 'continuar', 'continúa', 'continua',
            'adelante', 'hazlo', 'hacelo', 'dale', 'claro', 'correcto',
            'exacto', 'perfecto', 'por favor', 'procede por favor',
            # Inglés
            'yes', 'y', 'yep', 'yeah', 'sure', 'confirm', 'proceed',
            'continue', 'go ahead', 'do it', 'please proceed'
        ]
        
        # Verificar coincidencias exactas o en frases cortas
        if text_lower in confirmations:
            return True
        
        # Verificar si la frase completa contiene alguna confirmación clara
        for conf in confirmations:
            # Para palabras de 1 letra, solo buscar palabra completa
            if len(conf) == 1:
                if re.search(rf'\b{conf}\b', text_lower):
                    return True
            # Para palabras más largas, permitir match parcial
            elif conf in text_lower:
                return True
        
        return False
    
    def _is_rejection(self, text: str) -> bool:
        """
        Detecta si el texto del usuario es un rechazo
        
        Args:
            text: Texto del usuario
            
        Returns:
            True si es un rechazo, False si no
        """
        text_lower = text.lower().strip()
        
        # Palabras de rechazo en español e inglés
        rejections = [
            # Español
            'no', 'n', 'nop', 'nope', 'cancelar', 'cancela', 'detener',
            'detenlo', 'para', 'alto', 'stop', 'rechazar', 'rechazo',
            'mejor no', 'no proceder', 'no continuar', 'no gracias',
            # Inglés
            'cancel', 'reject', 'abort', 'halt', 'no thanks'
        ]
        
        # Verificar coincidencias
        if text_lower in rejections:
            return True
        
        for rej in rejections:
            if len(rej) == 1:
                if re.search(rf'\b{rej}\b', text_lower):
                    return True
            elif rej in text_lower:
                return True
        
        return False
    
    def process(self, user_input: str, context: Dict = None) -> Dict[str, Any]:
        """
        Procesa input del usuario a través de M.A.R.T.I.N.
        
        Maneja automáticamente:
        - Confirmaciones de acciones pendientes
        - Rechazos de acciones pendientes  
        - Nuevas consultas
        
        Args:
            user_input: Instrucción o consulta del usuario
            context: Contexto adicional (environment, user_role, etc.)
        
        Returns:
            Dict con la respuesta estructurada
        """
        if context is None:
            context = {}
        
        # ===== PASO 1: Verificar si hay acción pendiente =====
        if self.pending_action is not None:
            # Verificar si es una confirmación
            if self._is_confirmation(user_input):
                if self.verbose:
                    print("✅ Confirmación detectada - ejecutando acción pendiente")
                
                # Ejecutar la acción pendiente en modo DIRECT
                result = self.reasoning.direct_reasoning(
                    self.pending_action['original_input'],
                    self.pending_action['original_context']
                )
                
                # Agregar metadata
                result['confirmation'] = 'accepted'
                result['mode_explanation'] = f"Acción previamente en MODO {self.pending_action['mode']} confirmada por usuario. Ejecutando..."
                result['timestamp'] = datetime.now().isoformat()
                result['interaction_id'] = len(self.conversation_history)
                
                # Limpiar pending action
                self.pending_action = None
                
                # Guardar en historial
                self.conversation_history.append({
                    'input': user_input,
                    'context': context,
                    'result': result,
                    'timestamp': result['timestamp'],
                    'mode_selected': result['mode']
                })
                
                if self.verbose:
                    print(f"\n📤 ACCIÓN EJECUTADA")
                    print(result['message'][:200] + "...")
                    print(f"{'='*60}\n")
                
                return result
            
            # Verificar si es un rechazo
            elif self._is_rejection(user_input):
                if self.verbose:
                    print("❌ Rechazo detectado - cancelando acción pendiente")
                
                result = {
                    'mode': self.pending_action['mode'],
                    'status': 'cancelled',
                    'confirmation': 'rejected',
                    'message': "❌ Acción cancelada por el usuario.\n\n¿En qué más puedo ayudarte?",
                    'requires_user_action': False,
                    'timestamp': datetime.now().isoformat(),
                    'interaction_id': len(self.conversation_history),
                    'mode_explanation': 'Usuario rechazó la acción pendiente'
                }
                
                # Limpiar pending action
                self.pending_action = None
                
                # Guardar en historial
                self.conversation_history.append({
                    'input': user_input,
                    'context': context,
                    'result': result,
                    'timestamp': result['timestamp'],
                    'mode_selected': result['mode']
                })
                
                return result
            
            # Si no es ni confirmación ni rechazo, tratarlo como nueva consulta
            else:
                if self.verbose:
                    print("💬 Nueva consulta detectada - limpiando acción pendiente")
                self.pending_action = None
                # Continuar con el procesamiento normal
        
        # ===== PASO 2: Procesar nueva consulta =====
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"📥 INPUT: {user_input}")
            print(f"🌍 CONTEXT: {context}")
        
        # Seleccionar modo
        selected_mode = self.mode_selector.select_mode(user_input, context)
        
        if self.verbose:
            print(f"\n🧠 MODO SELECCIONADO: {selected_mode}")
            print(self.mode_selector.explain_last_decision())
        
        # Aplicar razonamiento según modo
        if selected_mode == "PASSIVE":
            result = self.reasoning.passive_reasoning(user_input, context)
        elif selected_mode == "DIRECT":
            result = self.reasoning.direct_reasoning(user_input, context)
        else:  # SAFE
            result = self.reasoning.safe_reasoning(user_input, context)
        
        # Agregar metadata
        result['mode_explanation'] = self.mode_selector.explain_last_decision()
        result['timestamp'] = datetime.now().isoformat()
        result['interaction_id'] = len(self.conversation_history)
        
        # Si requiere confirmación, guardar la acción pendiente
        if result.get('requires_user_action'):
            self.pending_action = {
                'mode': selected_mode,
                'original_input': user_input,
                'original_context': context,
                'result': result,
                'timestamp': result['timestamp']
            }
            
            if self.verbose:
                print("\n⏳ Acción pendiente de confirmación guardada")
        
        # Guardar en historial
        self.conversation_history.append({
            'input': user_input,
            'context': context,
            'result': result,
            'timestamp': result['timestamp'],
            'mode_selected': selected_mode
        })
        
        if self.verbose:
            print(f"\n📤 OUTPUT:")
            print(result['message'][:200] + "...")
            print(f"{'='*60}\n")
        
        return result
    
    def get_conversation_history(self) -> List[Dict]:
        """Retorna historial completo de la conversación"""
        return self.conversation_history
    
    def get_pending_action(self) -> Optional[Dict]:
        """Retorna la acción pendiente actual (si existe)"""
        return self.pending_action
    
    def reset(self):
        """Reinicia el agente (nueva sesión)"""
        self.conversation_history = []
        self.pending_action = None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if self.verbose:
            print(f"🔄 Sesión reiniciada - Nuevo Session ID: {self.session_id}")
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Retorna resumen de la sesión actual"""
        modes_used = {}
        confirmations = 0
        
        for interaction in self.conversation_history:
            mode = interaction.get('mode_selected', 'UNKNOWN')
            modes_used[mode] = modes_used.get(mode, 0) + 1
            
            if interaction['result'].get('confirmation'):
                confirmations += 1
        
        return {
            'session_id': self.session_id,
            'total_interactions': len(self.conversation_history),
            'modes_distribution': modes_used,
            'total_confirmations': confirmations,
            'has_pending_action': self.pending_action is not None,
            'llm_provider': self.llm_provider or 'simulado'
        }
    
    def export_conversation(self, format: str = 'json', filepath: str = None) -> str:
        """
        Exporta la conversación a archivo
        
        Args:
            format: 'json', 'text', o 'markdown'
            filepath: Ruta del archivo (opcional)
        
        Returns:
            Ruta del archivo generado
        """
        import json
        
        if filepath is None:
            ext = 'json' if format == 'json' else ('md' if format == 'markdown' else 'txt')
            filepath = f"martin_session_{self.session_id}.{ext}"
        
        if format == 'json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'session_id': self.session_id,
                    'timestamp': datetime.now().isoformat(),
                    'summary': self.get_session_summary(),
                    'conversation': self.conversation_history
                }, f, indent=2, ensure_ascii=False)
        
        elif format == 'markdown':
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# M.A.R.T.I.N. Session {self.session_id}\n\n")
                f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                summary = self.get_session_summary()
                f.write("## 📊 Resumen\n\n")
                f.write(f"- Total interacciones: {summary['total_interactions']}\n")
                f.write(f"- Confirmaciones: {summary['total_confirmations']}\n")
                f.write(f"- Modos usados: {summary['modes_distribution']}\n\n")
                
                f.write("## 💬 Conversación\n\n")
                for i, interaction in enumerate(self.conversation_history):
                    f.write(f"### Interacción {i+1}\n\n")
                    f.write(f"**Usuario:** {interaction['input']}\n\n")
                    f.write(f"**Modo:** {interaction['mode_selected']}\n\n")
                    f.write(f"**M.A.R.T.I.N.:**\n{interaction['result']['message']}\n\n")
                    f.write("---\n\n")
        
        else:  # text
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"M.A.R.T.I.N. Session {self.session_id}\n")
                f.write(f"{'='*60}\n\n")
                
                for i, interaction in enumerate(self.conversation_history):
                    f.write(f"[{i+1}] Usuario: {interaction['input']}\n")
                    f.write(f"    Modo: {interaction['mode_selected']}\n")
                    f.write(f"    M.A.R.T.I.N.: {interaction['result']['message']}\n")
                    f.write("-"*60 + "\n\n")
        
        return filepath
    
    def get_stats(self) -> Dict[str, Any]:
        """Alias de get_session_summary para compatibilidad"""
        return self.get_session_summary()


# Test básico
if __name__ == "__main__":
    print("🧪 TESTING MARTIN AGENT CON SISTEMA DE CONFIRMACIÓN\n")
    
    agent = MARTINAgent(use_llm=False, verbose=True)
    
    # Test 1: Modo pasivo con confirmación
    print("\n" + "━"*60)
    print("TEST 1: Modo Pasivo + Confirmación")
    print("━"*60)
    
    result1 = agent.process("Ayúdame con SOC 2")
    print(f"\n✓ Requiere acción: {result1.get('requires_user_action')}")
    print(f"✓ Acción pendiente: {agent.get_pending_action() is not None}")
    
    # Confirmar
    result2 = agent.process("sí, continúa")
    print(f"\n✓ Confirmación procesada: {result2.get('confirmation')}")
    print(f"✓ Acción pendiente limpiada: {agent.get_pending_action() is None}")
    
    # Test 2: Rechazo
    print("\n" + "━"*60)
    print("TEST 2: Modo Pasivo + Rechazo")
    print("━"*60)
    
    result3 = agent.process("Quiero cambiar mi estrategia de compliance")
    result4 = agent.process("no, mejor no")
    print(f"\n✓ Rechazo procesado: {result4.get('confirmation')}")
    
    # Test 3: Nueva consulta sin confirmar
    print("\n" + "━"*60)
    print("TEST 3: Nueva consulta interrumpe confirmación")
    print("━"*60)
    
    result5 = agent.process("Genera una política de seguridad")
    result6 = agent.process("¿Qué es SOC 2?")  # Nueva pregunta, no confirmación
    print(f"\n✓ Nueva consulta procesada correctamente")
    
    print("\n✅ Tests completados!")
    print(f"\n📊 Resumen: {agent.get_session_summary()}")