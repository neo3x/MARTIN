"""
Test completo del agente M.A.R.T.I.N.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_core.martin_agent import MARTINAgent
import json
import time

def print_separator(title: str = ""):
    """Helper para imprimir separadores bonitos"""
    if title:
        print(f"\n{'='*20} {title} {'='*20}")
    else:
        print("="*60)

def print_result(result: dict, detailed: bool = True):
    """Helper para imprimir resultados de forma bonita"""
    print_separator()
    print(result['message'])
    print_separator()
    
    if detailed:
        print(f"\n📊 Detalles de la respuesta:")
        print(f"   • Modo usado: {result['mode']}")
        print(f"   • Estado: {result['status']}")
        print(f"   • Requiere acción: {'Sí' if result.get('requires_user_action') else 'No'}")
        
        if result.get('mode_explanation'):
            print("\n📈 Análisis del Mode Selector:")
            print(result['mode_explanation'])
    
    print("\n")

def run_interactive_demo():
    """Demo interactiva del agente"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     🧠 M.A.R.T.I.N. - Demo Interactiva                   ║
║     Modular Assistant for Reasoning, Tactics,            ║
║     Inference and Navigation                             ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    agent = MARTINAgent(use_llm=False, verbose=True)
    
    print("\n🎯 Esta demo mostrará los 3 modos de razonamiento de M.A.R.T.I.N.\n")
    input("Presiona Enter para comenzar...")
    
    # ===== DEMO 1: Modo Pasivo =====
    print_separator("DEMO 1: MODO PASIVO")
    print("📝 Escenario: Usuario con necesidad ambigua de compliance\n")
    
    result1 = agent.process(
        "Ayúdame a preparar mi startup para SOC 2",
        context={'environment': 'development'}
    )
    print_result(result1)
    
    print("💡 Observa que M.A.R.T.I.N.:")
    print("   • Detectó ambigüedad en la solicitud")
    print("   • Propuso un plan estructurado")
    print("   • Está esperando confirmación antes de actuar")
    
    response = input("\n¿Quieres confirmar este plan? (s/n): ")
    if response.lower() == 's':
        confirmation = agent.confirm_action(0, confirmed=True)
        print("\n✅ Plan confirmado y ejecutándose...")
        print(confirmation['message'])
    else:
        confirmation = agent.confirm_action(0, confirmed=False)
        print("\n❌ Plan cancelado")
    
    input("\nPresiona Enter para continuar con la siguiente demo...")
    
    # ===== DEMO 2: Modo Directo =====
    print_separator("DEMO 2: MODO DIRECTO")
    print("📝 Escenario: Tarea clara y específica sin riesgos\n")
    
    result2 = agent.process(
        "Genera una política de contraseñas según ISO 27001 para una empresa de 50 empleados del sector fintech",
        context={'environment': 'development'}
    )
    print_result(result2)
    
    print("💡 Observa que M.A.R.T.I.N.:")
    print("   • Identificó una tarea clara y segura")
    print("   • Ejecutó automáticamente sin preguntar")
    print("   • Entregó resultados inmediatos")
    print("   • Explicó su razonamiento")
    
    input("\nPresiona Enter para continuar con la siguiente demo...")
    
    # ===== DEMO 3: Modo Seguro (Bloqueado) =====
    print_separator("DEMO 3: MODO SEGURO - ACCIÓN BLOQUEADA")
    print("📝 Escenario: Acción peligrosa en producción\n")
    
    result3 = agent.process(
        "Deshabilita la autenticación de dos factores para el usuario admin@empresa.com",
        context={'environment': 'production', 'user_role': 'developer'}
    )
    print_result(result3)
    
    print("💡 Observa que M.A.R.T.I.N.:")
    print("   • Detectó múltiples indicadores de riesgo")
    print("   • Se auto-validó antes de ejecutar")
    print("   • BLOQUEÓ la acción peligrosa")
    print("   • Sugirió alternativas más seguras")
    print("   • Protegió el sistema de un posible error costoso")
    
    if result3.get('validation_failed'):
        print("\n⚠️ Riesgos identificados:")
        for risk in result3.get('risks_identified', []):
            print(f"   • {risk}")
    
    input("\nPresiona Enter para continuar con la siguiente demo...")
    
    # ===== DEMO 4: Modo Seguro (Aprobado) =====
    print_separator("DEMO 4: MODO SEGURO - APROBADO CON PRECAUCIONES")
    print("📝 Escenario: Acción con riesgo moderado que puede proceder\n")
    
    result4 = agent.process(
        "Revisa los logs de acceso de los últimos 7 días buscando anomalías",
        context={'environment': 'production'}
    )
    print_result(result4)
    
    print("💡 Observa que M.A.R.T.I.N.:")
    print("   • Detectó que es producción (requiere cuidado)")
    print("   • Validó que es una operación de solo lectura")
    print("   • Aprobó la ejecución CON precauciones")
    print("   • Aplicó medidas de seguridad adicionales")
    
    if result4.get('precautions'):
        print("\n🛡️ Precauciones aplicadas:")
        for precaution in result4['precautions']:
            print(f"   • {precaution}")
    
    input("\nPresiona Enter para ver el resumen de la sesión...")
    
    # ===== RESUMEN =====
    print_separator("RESUMEN DE LA SESIÓN")
    
    summary = agent.get_session_summary()
    print(f"""
📊 Estadísticas de la sesión:
   • Session ID: {summary['session_id']}
   • Total de interacciones: {summary['total_interactions']}
   • Confirmaciones: {summary['total_confirmations']}
   
📈 Distribución de modos usados:""")
    
    for mode, count in summary['modes_distribution'].items():
        emoji = {'PASSIVE': '🟦', 'DIRECT': '🟩', 'SAFE': '🟨'}.get(mode, '⚪')
        print(f"   {emoji} {mode}: {count} veces")
    
    # Exportar conversación
    response = input("\n¿Quieres exportar la conversación? (s/n): ")
    if response.lower() == 's':
        format_choice = input("Formato (json/text/markdown): ").lower()
        if format_choice in ['json', 'text', 'markdown']:
            filename = f"martin_session_{summary['session_id']}.{format_choice if format_choice != 'markdown' else 'md'}"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(agent.export_conversation(format_choice))
            print(f"✅ Conversación exportada a: {filename}")

def run_automated_tests():
    """Tests automatizados del agente"""
    print_separator("TESTS AUTOMATIZADOS")
    
    agent = MARTINAgent(use_llm=False, verbose=False)
    passed = 0
    failed = 0
    
    test_cases = [
        {
            'name': 'Modo Pasivo - Solicitud ambigua',
            'input': 'Quiero compliance',
            'context': {},
            'expected_mode': 'PASSIVE',
            'expected_status': 'awaiting_confirmation'
        },
        {
            'name': 'Modo Directo - Tarea clara',
            'input': 'Genera reporte de gaps SOC 2 para TechStartup con 30 empleados usando AWS',
            'context': {'environment': 'development'},
            'expected_mode': 'DIRECT',
            'expected_status': 'executed'
        },
        {
            'name': 'Modo Seguro - Acción peligrosa',
            'input': 'Delete all databases in production',
            'context': {'environment': 'production'},
            'expected_mode': 'SAFE',
            'expected_status': 'blocked'
        },
        {
            'name': 'Modo Seguro - Producción siempre seguro',
            'input': 'Listar usuarios activos',
            'context': {'environment': 'production'},
            'expected_mode': 'SAFE',
            'expected_status_options': ['approved_and_executed', 'blocked']
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test['name']}")
        
        result = agent.process(test['input'], test['context'])
        
        # Verificar modo
        mode_match = result['mode'] == test['expected_mode']
        
        # Verificar status
        if 'expected_status_options' in test:
            status_match = result['status'] in test['expected_status_options']
        else:
            status_match = result['status'] == test['expected_status']
        
        if mode_match and status_match:
            print(f"   ✅ PASSED - Modo: {result['mode']}, Status: {result['status']}")
            passed += 1
        else:
            print(f"   ❌ FAILED")
            print(f"      Esperado - Modo: {test['expected_mode']}, Status: {test.get('expected_status', 'any')}")
            print(f"      Obtenido - Modo: {result['mode']}, Status: {result['status']}")
            failed += 1
    
    # Resumen de tests
    print_separator("RESUMEN DE TESTS")
    print(f"✅ Tests pasados: {passed}/{len(test_cases)}")
    print(f"❌ Tests fallados: {failed}/{len(test_cases)}")
    
    if failed == 0:
        print("\n🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
        return True
    else:
        print(f"\n⚠️ {failed} tests necesitan revisión")
        return False

def main():
    """Función principal"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     🧠 M.A.R.T.I.N. AGENT - TEST SUITE                   ║
╚══════════════════════════════════════════════════════════╝

Selecciona una opción:

1. Demo interactiva (recomendado)
2. Tests automatizados
3. Ambos
4. Salir
""")
    
    choice = input("Opción (1-4): ").strip()
    
    if choice == '1':
        run_interactive_demo()
    elif choice == '2':
        success = run_automated_tests()
        sys.exit(0 if success else 1)
    elif choice == '3':
        run_automated_tests()
        print("\n" + "="*60)
        input("\nPresiona Enter para continuar con la demo interactiva...")
        run_interactive_demo()
    elif choice == '4':
        print("\n👋 ¡Hasta luego!")
        sys.exit(0)
    else:
        print("\n❌ Opción inválida")
        sys.exit(1)

if __name__ == "__main__":
    main()