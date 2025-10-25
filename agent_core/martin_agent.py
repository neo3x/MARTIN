"""
M.A.R.T.I.N. Agent - Integración completa del sistema
"""
import sys
import os
from typing import Dict, Any, List
from datetime import datetime

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
        self.use_llm = use_llm
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if self.verbose:
            print(f"🧠 M.A.R.T.I.N. Agent iniciado")
            print(f"   Session ID: {self.session_id}")
            print(f"   Modo LLM: {'Activado ✓' if use_llm else 'Simulado (sin API key)'}")
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
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"📥 INPUT: {user_input}")
            print(f"🌍 CONTEXT: {context}")
        
        # Paso 1: Decidir modo
        selected_mode = self.mode_selector.select_mode(user_input, context)
        
        if self.verbose:
            print(f"\n🧠 MODO SELECCIONADO: {selected_mode}")
            print(self.mode_selector.explain_last_decision())
        
        # Paso 2: Aplicar razonamiento según modo
        if selected_mode == "PASSIVE":
            result = self.reasoning.passive_reasoning(user_input, context)
        elif selected_mode == "DIRECT":
            result = self.reasoning.direct_reasoning(user_input, context)
        else:  # SAFE
            result = self.reasoning.safe_reasoning(user_input, context)
        
        # Agregar explicación del mode selector
        result['mode_explanation'] = self.mode_selector.explain_last_decision()
        result['timestamp'] = datetime.now().isoformat()
        
        # Guardar en historial
        self.conversation_history.append({
            'input': user_input,
            'context': context,
            'result': result,
            'timestamp': result['timestamp']
        })
        
        if self.verbose:
            print(f"\n📤 OUTPUT:")
            print(result['message'])
            print(f"{'='*60}\n")
        
        return result
    
    def get_conversation_history(self) -> List[Dict]:
        """Retorna historial completo de la conversación"""
        return self.conversation_history
    
    def export_conversation(self, filepath: str = None) -> str:
        """
        Exporta la conversación a un archivo
        
        Args:
            filepath: Ruta del archivo. Si None, usa nombre por defecto.
        
        Returns:
            Ruta del archivo exportado
        """
        if filepath is None:
            filepath = f"martin_conversation_{self.session_id}.txt"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("M.A.R.T.I.N. - Conversación Exportada\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Total de interacciones: {len(self.conversation_history)}\n")
            f.write("="*80 + "\n\n")
            
            for i, entry in enumerate(self.conversation_history, 1):
                f.write(f"\n{'─'*80}\n")
                f.write(f"Interacción #{i}\n")
                f.write(f"Timestamp: {entry['timestamp']}\n")
                f.write(f"{'─'*80}\n\n")
                
                f.write(f"👤 Usuario:\n{entry['input']}\n\n")
                f.write(f"🌍 Contexto:\n{entry['context']}\n\n")
                f.write(f"🧠 Modo usado:\n{entry['result']['mode']}\n\n")
                f.write(f"🤖 M.A.R.T.I.N.:\n{entry['result']['message']}\n\n")
        
        return filepath
    
    def reset(self):
        """Reinicia el agente (limpia historial)"""
        self.conversation_history = []
        self.mode_selector.decision_log = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if self.verbose:
            print("🔄 M.A.R.T.I.N. reiniciado")
            print(f"   Nuevo Session ID: {self.session_id}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de uso"""
        if not self.conversation_history:
            return {
                "total_interactions": 0,
                "modes_used": {},
                "session_id": self.session_id
            }
        
        modes_count = {}
        for entry in self.conversation_history:
            mode = entry['result']['mode']
            modes_count[mode] = modes_count.get(mode, 0) + 1
        
        return {
            "total_interactions": len(self.conversation_history),
            "modes_used": modes_count,
            "session_id": self.session_id,
            "llm_mode": "Real" if self.use_llm else "Simulado"
        }


# Test del agente completo
if __name__ == "__main__":
    print("🧪 TESTING M.A.R.T.I.N. AGENT\n")
    
    # Crear agente (sin LLM para testing rápido)
    agent = MARTINAgent(use_llm=False, verbose=True)
    
    # Test 1: Modo PASSIVE
    print("\n" + "🔵"*30)
    print("TEST 1: Tarea ambigua → Debe activar MODO PASIVO")
    print("🔵"*30)
    result1 = agent.process("Ayúdame a preparar mi startup para SOC 2")
    assert result1['mode'] == 'PASSIVE'
    assert result1['requires_user_action'] == True
    print("✅ Test 1 PASSED\n")
    
    # Test 2: Modo DIRECT
    print("\n" + "🟢"*30)
    print("TEST 2: Tarea clara → Debe activar MODO DIRECTO")
    print("🟢"*30)
    result2 = agent.process("Genera una política de respuesta a incidentes según SOC 2")
    assert result2['mode'] == 'DIRECT'
    assert result2['requires_user_action'] == False
    print("✅ Test 2 PASSED\n")
    
    # Test 3: Modo SAFE (bloqueado)
    print("\n" + "🟡"*30)
    print("TEST 3: Acción peligrosa → Debe activar MODO SEGURO y BLOQUEAR")
    print("🟡"*30)
    result3 = agent.process(
        "Deshabilita todos los usuarios administradores",
        context={'environment': 'production'}
    )
    assert result3['mode'] == 'SAFE'
    assert result3['status'] == 'blocked'
    print("✅ Test 3 PASSED\n")
    
    # Mostrar estadísticas
    print("\n" + "📊"*30)
    print("ESTADÍSTICAS DE LA SESIÓN")
    print("📊"*30)
    stats = agent.get_stats()
    print(f"Total de interacciones: {stats['total_interactions']}")
    print(f"Modos usados: {stats['modes_used']}")
    print(f"Session ID: {stats['session_id']}")
    
    # Exportar conversación
    print("\n📁 Exportando conversación...")
    filepath = agent.export_conversation()
    print(f"✅ Conversación exportada a: {filepath}")
    
    print("\n🎉 TODOS LOS TESTS PASARON!")