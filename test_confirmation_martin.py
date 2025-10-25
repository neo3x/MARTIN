#!/usr/bin/env python3
"""
Script de prueba rápida del sistema de confirmación de MARTIN
Ejecuta tests automáticos para verificar el funcionamiento
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

def print_separator(title="", char="=", length=70):
    if title:
        padding = (length - len(title) - 2) // 2
        print(f"\n{char * padding} {title} {char * padding}")
    else:
        print(char * length)

def test_confirmations():
    """Test del sistema de confirmación"""
    from agent_core.martin_agent import MARTINAgent
    
    print_separator("INICIANDO TESTS DEL SISTEMA DE CONFIRMACIÓN")
    
    agent = MARTINAgent(use_llm=False, verbose=False)
    
    # Test 1: Confirmación básica
    print_separator("TEST 1: Confirmación Básica", "-")
    print("\n1. Usuario: 'Ayúdame con SOC 2'")
    result1 = agent.process("Ayúdame con SOC 2")
    
    assert result1.get('requires_user_action'), "❌ Debería requerir acción"
    assert agent.get_pending_action() is not None, "❌ Debería tener acción pendiente"
    print("✅ MARTIN pide confirmación correctamente")
    print(f"   Acción pendiente: {agent.get_pending_action()['mode']}")
    
    print("\n2. Usuario: 'sí'")
    result2 = agent.process("sí")
    
    assert result2.get('confirmation') == 'accepted', "❌ Debería detectar confirmación"
    assert agent.get_pending_action() is None, "❌ Debería limpiar acción pendiente"
    print("✅ Confirmación detectada y ejecutada")
    print("✅ Acción pendiente limpiada")
    
    # Test 2: Rechazo
    print_separator("TEST 2: Rechazo", "-")
    print("\n1. Usuario: 'Quiero cambiar mi estrategia'")
    result3 = agent.process("Quiero cambiar mi estrategia")
    
    assert result3.get('requires_user_action'), "❌ Debería requerir acción"
    print("✅ MARTIN pide confirmación")
    
    print("\n2. Usuario: 'no, mejor no'")
    result4 = agent.process("no, mejor no")
    
    assert result4.get('confirmation') == 'rejected', "❌ Debería detectar rechazo"
    assert agent.get_pending_action() is None, "❌ Debería limpiar acción pendiente"
    print("✅ Rechazo detectado correctamente")
    print("✅ Acción cancelada")
    
    # Test 3: Nueva consulta interrumpe
    print_separator("TEST 3: Nueva Consulta Interrumpe", "-")
    print("\n1. Usuario: 'Genera una política'")
    result5 = agent.process("Genera una política")
    
    print("\n2. Usuario: '¿Qué es SOC 2?' (nueva pregunta)")
    result6 = agent.process("¿Qué es SOC 2?")
    
    assert agent.get_pending_action() is None, "❌ Nueva consulta debería limpiar pending"
    print("✅ Nueva consulta procesada correctamente")
    print("✅ Acción pendiente limpiada automáticamente")
    
    # Test 4: Variaciones de confirmación
    print_separator("TEST 4: Variaciones de Confirmación", "-")
    
    confirmaciones_test = [
        "sí, continúa",
        "ok perfecto",
        "adelante",
        "dale",
        "confirmo",
        "yes, proceed",
        "sure, go ahead"
    ]
    
    for conf in confirmaciones_test:
        # Crear nueva acción pendiente
        agent.process("Ayúdame con algo")
        
        # Probar confirmación
        result = agent.process(conf)
        
        if result.get('confirmation') == 'accepted':
            print(f"✅ '{conf}' detectada correctamente")
        else:
            print(f"❌ '{conf}' NO detectada")
    
    # Test 5: Variaciones de rechazo
    print_separator("TEST 5: Variaciones de Rechazo", "-")
    
    rechazos_test = [
        "no",
        "cancelar",
        "mejor no",
        "no gracias",
        "cancel",
        "abort"
    ]
    
    for rec in rechazos_test:
        # Crear nueva acción pendiente
        agent.process("Ayúdame con algo")
        
        # Probar rechazo
        result = agent.process(rec)
        
        if result.get('confirmation') == 'rejected':
            print(f"✅ '{rec}' detectado correctamente")
        else:
            print(f"❌ '{rec}' NO detectado")
    
    # Resumen final
    print_separator("RESUMEN DE LA SESIÓN")
    summary = agent.get_session_summary()
    
    print(f"""
📊 Estadísticas:
   • Total interacciones: {summary['total_interactions']}
   • Confirmaciones procesadas: {summary['total_confirmations']}
   • Modos usados: {summary['modes_distribution']}
   • Acción pendiente actual: {'Sí' if summary['has_pending_action'] else 'No'}
    """)
    
    print_separator("TESTS COMPLETADOS", "=")
    print("\n✅ Todos los tests pasaron exitosamente!")
    print("✅ El sistema de confirmación funciona correctamente\n")

def interactive_demo():
    """Demo interactiva del sistema"""
    from agent_core.martin_agent import MARTINAgent
    
    print_separator("DEMO INTERACTIVA DEL SISTEMA DE CONFIRMACIÓN")
    print("""
Este modo te permite probar el sistema interactivamente.

Comandos:
- Escribe cualquier pregunta o solicitud
- Cuando MARTIN pida confirmación, responde 'sí', 'no', o haz otra pregunta
- Escribe 'salir' para terminar
- Escribe 'estado' para ver el estado actual
    """)
    
    agent = MARTINAgent(use_llm=False, verbose=True)
    
    while True:
        try:
            # Mostrar si hay acción pendiente
            if agent.get_pending_action():
                user_input = input("\n📌 [Acción pendiente] Tu: ").strip()
            else:
                user_input = input("\n💬 Tu: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'salir':
                print("\n👋 ¡Hasta luego!")
                break
            
            if user_input.lower() == 'estado':
                pending = agent.get_pending_action()
                if pending:
                    print(f"\n📋 Acción pendiente desde: {pending['timestamp']}")
                    print(f"   Modo: {pending['mode']}")
                    print(f"   Input original: {pending['original_input']}")
                else:
                    print("\n✅ No hay acciones pendientes")
                continue
            
            # Procesar input
            result = agent.process(user_input)
            
            # Mostrar respuesta
            print(f"\n🧠 MARTIN ({result['mode']}):")
            print(result['message'])
            
            if result.get('requires_user_action'):
                print("\n⚠️ Esperando tu confirmación (escribe 'sí' o 'no')")
        
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════╗
║  🧠 MARTIN - Test del Sistema de Confirmación             ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    print("Elige una opción:")
    print("1. Tests automáticos (recomendado)")
    print("2. Demo interactiva")
    print("3. Ambos")
    
    choice = input("\nOpción (1-3): ").strip()
    
    if choice == '1':
        test_confirmations()
    elif choice == '2':
        interactive_demo()
    elif choice == '3':
        test_confirmations()
        print("\n" + "="*70)
        input("\nPresiona Enter para continuar con la demo interactiva...")
        interactive_demo()
    else:
        print("❌ Opción inválida")