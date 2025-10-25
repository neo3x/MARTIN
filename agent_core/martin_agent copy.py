"""
M.A.R.T.I.N. Agent - Integración completa con soporte multi-LLM
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
            Dict con la respuesta estructurada
        """
        if context is None:
            context = {}
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"📥 INPUT: {user_input}")
            print(f"🌍 CONTEXT: {context}")
        
        # Paso 1: Seleccionar modo
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
        
        # Agregar metadata
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
        """Retorna historial completo"""
        return self.conversation_history
    
    def export_conversation(self, filepath: str = None) -> str:
        """Exporta conversación a archivo"""
        if filepath is None:
            filepath = f"martin_conversation_{self.session_id}.txt"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("M.A.R.T.I.N. - Conversación Exportada\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Total: {len(self.conversation_history)} interacciones\n")
            if self.llm_provider:
                provider_name = {
                    "openai": "OpenAI GPT-4",
                    "claude": "Anthropic Claude 3.5 Sonnet"
                }.get(self.llm_provider, "Simulado")
                f.write(f"LLM usado: {provider_name}\n")
            f.write("="*80 + "\n\n")
            
            for i, entry in enumerate(self.conversation_history, 1):
                f.write(f"\n{'─'*80}\n")
                f.write(f"Interacción #{i}\n")
                f.write(f"Timestamp: {entry['timestamp']}\n")
                f.write(f"{'─'*80}\n\n")
                f.write(f"👤 Usuario:\n{entry['input']}\n\n")
                f.write(f"🌍 Contexto:\n{entry['context']}\n\n")
                f.write(f"🧠 Modo: {entry['result']['mode']}\n\n")
                f.write(f"🤖 M.A.R.T.I.N.:\n{entry['result']['message']}\n\n")
        
        return filepath
    
    def reset(self):
        """Reinicia el agente"""
        self.conversation_history = []
        self.mode_selector.decision_log = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        if self.verbose:
            print(f"🔄 M.A.R.T.I.N. reiniciado - Session ID: {self.session_id}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas"""
        if not self.conversation_history:
            return {
                "total_interactions": 0,
                "modes_used": {},
                "session_id": self.session_id,
                "llm_provider": self.llm_provider or "simulado"
            }
        
        modes_count = {}
        for entry in self.conversation_history:
            mode = entry['result']['mode']
            modes_count[mode] = modes_count.get(mode, 0) + 1
        
        return {
            "total_interactions": len(self.conversation_history),
            "modes_used": modes_count,
            "session_id": self.session_id,
            "llm_provider": self.llm_provider or "simulado"
        }


# Test
if __name__ == "__main__":
    print("🧪 TESTING M.A.R.T.I.N. AGENT\n")
    
    agent = MARTINAgent(use_llm=False, verbose=True)
    
    # Test 1: PASSIVE
    print("\n" + "🟦"*30)
    print("TEST 1: MODO PASIVO")
    print("🟦"*30)
    result1 = agent.process("Ayúdame con SOC 2")
    assert result1['mode'] == 'PASSIVE'
    print("✅ Test 1 PASSED\n")
    
    # Test 2: DIRECT
    print("\n" + "🟩"*30)
    print("TEST 2: MODO DIRECTO")
    print("🟩"*30)
    result2 = agent.process("Genera política de passwords")
    assert result2['mode'] == 'DIRECT'
    print("✅ Test 2 PASSED\n")
    
    # Test 3: SAFE
    print("\n" + "🟨"*30)
    print("TEST 3: MODO SEGURO")
    print("🟨"*30)
    result3 = agent.process("Delete all users", {'environment': 'production'})
    assert result3['mode'] == 'SAFE'
    print("✅ Test 3 PASSED\n")
    
    # Stats
    print("\n📊 ESTADÍSTICAS:")
    stats = agent.get_stats()
    print(f"Total: {stats['total_interactions']}")
    print(f"Modos: {stats['modes_used']}")
    print(f"LLM: {stats['llm_provider']}")
    
    # Export
    filepath = agent.export_conversation()
    print(f"\n📁 Exportado a: {filepath}")
    
    print("\n🎉 TODOS LOS TESTS PASARON!")