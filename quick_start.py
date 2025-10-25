#!/usr/bin/env python3
"""
Script de inicio rápido para probar M.A.R.T.I.N.
Ejecuta los 3 casos de demo principales
"""
import sys
import os
from pathlib import Path

# Agregar directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from agent_core.martin_agent import MARTINAgent

def print_separator(char="=", length=70):
    print(char * length)

def run_demo():
    """Ejecuta demostración de los 3 modos"""
    
    print_separator("=")
    print("🧠 M.A.R.T.I.N. - DEMOSTRACIÓN RÁPIDA")
    print_separator("=")
    print()
    
    # Verificar API key
    use_llm = os.getenv('OPENAI_API_KEY') is not None
    
    if use_llm:
        print("✅ API Key detectada - Usando GPT-4 (respuestas reales)")
    else:
        print("⚠️  Sin API Key - Usando modo simulado (respuestas de ejemplo)")
        print("   Para usar GPT-4, configura OPENAI_API_KEY en .env")
    
    print()
    print("Presiona Enter para continuar con cada demo...")
    print()
    
    # Crear agente
    agent = MARTINAgent(use_llm=use_llm, verbose=False)
    
    # DEMO 1: Modo Pasivo
    input("▶️  Demo 1: Modo Pasivo (presiona Enter)...")
    print()
    print_separator("🟦", 70)
    print("DEMO 1: MODO PASIVO - Tarea ambigua")
    print_separator("🟦", 70)
    print()
    
    result1 = agent.process(
        "Ayúdame a preparar mi startup para certificación SOC 2",
        context={'environment': 'development'}
    )
    
    print("💬 Usuario:")
    print("   'Ayúdame a preparar mi startup para certificación SOC 2'")
    print()
    print("🧠 M.A.R.T.I.N. responde:")
    print(result1['message'])
    print()
    print("📌 Lo que pasó:")
    print("   • M.A.R.T.I.N. detectó que la tarea es amplia y ambigua")
    print("   • Activó MODO PASIVO")
    print("   • Propuso un plan estructurado")
    print("   • Esperando confirmación del usuario antes de actuar")
    print()
    
    # DEMO 2: Modo Directo
    input("▶️  Demo 2: Modo Directo (presiona Enter)...")
    print()
    print_separator("🟩", 70)
    print("DEMO 2: MODO DIRECTO - Tarea clara y segura")
    print_separator("🟩", 70)
    print()
    
    result2 = agent.process(
        "Genera una política de respuesta a incidentes según SOC 2",
        context={'environment': 'development'}
    )
    
    print("💬 Usuario:")
    print("   'Genera una política de respuesta a incidentes según SOC 2'")
    print()
    print("🧠 M.A.R.T.I.N. responde:")
    print(result2['message'])
    print()
    print("📌 Lo que pasó:")
    print("   • M.A.R.T.I.N. detectó que la tarea es clara y específica")
    print("   • Activó MODO DIRECTO")
    print("   • Ejecutó automáticamente sin preguntar")
    print("   • Entregó resultado y explicó su razonamiento")
    print()
    
    # DEMO 3: Modo Seguro
    input("▶️  Demo 3: Modo Seguro (presiona Enter)...")
    print()
    print_separator("🟨", 70)
    print("DEMO 3: MODO SEGURO - Acción peligrosa en producción")
    print_separator("🟨", 70)
    print()
    
    result3 = agent.process(
        "Deshabilita la autenticación de dos factores para admin@empresa.com",
        context={'environment': 'production'}
    )
    
    print("💬 Usuario:")
    print("   'Deshabilita la autenticación de dos factores para admin@empresa.com'")
    print("   Ambiente: PRODUCTION")
    print()
    print("🧠 M.A.R.T.I.N. responde:")
    print(result3['message'])
    print()
    print("📌 Lo que pasó:")
    print("   • M.A.R.T.I.N. detectó acción de alto riesgo en producción")
    print("   • Activó MODO SEGURO")
    print("   • Se auto-validó antes de actuar")
    print("   • BLOQUEÓ la acción por riesgos detectados")
    print("   • Sugirió alternativa más segura")
    print()
    
    # Resumen final
    print_separator("=")
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print_separator("=")
    print()
    print("🎯 RESUMEN:")
    print("   M.A.R.T.I.N. adaptó su comportamiento según el contexto:")
    print()
    print("   🟦 PASIVO → Pregunta antes de actuar")
    print("   🟩 DIRECTO → Ejecuta autónomamente")
    print("   🟨 SEGURO → Auto-valida y protege")
    print()
    print("📊 Estadísticas:")
    stats = agent.get_stats()
    print(f"   Total de interacciones: {stats['total_interactions']}")
    print(f"   Modos usados: {stats['modes_used']}")
    print()
    
    # Opciones siguientes
    print("🚀 PRÓXIMOS PASOS:")
    print()
    print("   1. Para interfaz web interactiva:")
    print("      python interface/gradio_app.py")
    print()
    print("   2. Para CLI interactivo:")
    print("      python main.py --mode cli")
    print()
    print("   3. Para configurar tu API key:")
    print("      - Copia .env.example a .env")
    print("      - Agrega tu OPENAI_API_KEY")
    print()


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrumpida por el usuario")
        print("👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error durante la demo: {e}")
        print("💡 Tip: Asegúrate de haber instalado las dependencias:")
        print("   pip install -r requirements.txt")