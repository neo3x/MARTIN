#!/usr/bin/env python3
"""
M.A.R.T.I.N. - Modular Assistant for Reasoning, Tactics, Inference and Navigation
Punto de entrada principal del sistema
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from agent_core.martin_agent import MARTINAgent

def print_banner():
    """Imprime el banner de M.A.R.T.I.N."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     🧠 M.A.R.T.I.N.                                                         ║
║     Modular Assistant for Reasoning, Tactics, Inference and Navigation      ║
║                                                                              ║
║     Agente de IA con razonamiento adaptativo tri-modal                      ║
║     Desarrollado para The Agent Hackathon 2025                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_cli_mode():
    """Ejecuta M.A.R.T.I.N. en modo CLI interactivo"""
    print_banner()
    
    # Verificar configuración
    use_llm = os.getenv('OPENAI_API_KEY') is not None
    if not use_llm:
        print("⚠️  No se detectó OPENAI_API_KEY. Ejecutando en modo simulado.")
        print("   Para usar GPT-4, configura tu API key en el archivo .env\n")
    else:
        print("✅ API Key detectada. Usando GPT-4 para respuestas.\n")
    
    # Inicializar agente
    agent = MARTINAgent(use_llm=use_llm, verbose=False)
    
    print("Comandos disponibles:")
    print("  /help     - Muestra esta ayuda")
    print("  /mode     - Muestra información sobre los modos")
    print("  /history  - Muestra el historial de la conversación")
    print("  /export   - Exporta la conversación")
    print("  /reset    - Reinicia el agente")
    print("  /quit     - Salir")
    print("\n" + "="*80 + "\n")
    
    # Seleccionar ambiente
    print("Selecciona el ambiente de trabajo:")
    print("1. Development (por defecto)")
    print("2. Staging")
    print("3. Production")
    env_choice = input("\nAmbiente (1-3) [1]: ").strip() or '1'
    
    environment = {
        '1': 'development',
        '2': 'staging',
        '3': 'production'
    }.get(env_choice, 'development')
    
    print(f"\n🌍 Ambiente seleccionado: {environment}")
    if environment == 'production':
        print("⚠️  ADVERTENCIA: En producción, M.A.R.T.I.N. usará el modo SEGURO por defecto")
    
    print("\n" + "="*80)
    print("\n💬 Puedes empezar a conversar con M.A.R.T.I.N.\n")
    
    context = {'environment': environment}
    pending_confirmation = None
    
    while True:
        try:
            # Prompt diferente si hay acción pendiente
            if pending_confirmation:
                user_input = input("📌 Acción pendiente > ").strip()
            else:
                user_input = input("Tu > ").strip()
            
            if not user_input:
                continue
            
            # Procesar comandos especiales
            if user_input.startswith('/'):
                handle_command(user_input, agent, context)
                continue
            
            # Si hay confirmación pendiente
            if pending_confirmation:
                if user_input.lower() in ['sí', 'si', 's', 'yes', 'y', 'confirmar', 'ok']:
                    result = agent.confirm_action(pending_confirmation['id'], confirmed=True)
                    print("\n✅ Acción confirmada y ejecutada")
                    pending_confirmation = None
                elif user_input.lower() in ['no', 'n', 'cancelar', 'cancel']:
                    result = agent.confirm_action(pending_confirmation['id'], confirmed=False)
                    print("\n❌ Acción cancelada")
                    pending_confirmation = None
                else:
                    # No es confirmación, es un nuevo input
                    pending_confirmation = None
                    result = agent.process(user_input, context)
            else:
                # Procesar input normal
                result = agent.process(user_input, context)
            
            # Mostrar respuesta
            print_response(result)
            
            # Verificar si requiere confirmación
            if result.get('requires_user_action'):
                pending_confirmation = {
                    'id': result['interaction_id'],
                    'mode': result['mode']
                }
                print("\n❓ ¿Deseas proceder? (sí/no)")
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Intenta de nuevo o usa /help para ver los comandos disponibles")

def handle_command(command: str, agent: MARTINAgent, context: dict):
    """Maneja comandos especiales del CLI"""
    
    if command == '/help':
        print("""
Comandos disponibles:
  /help     - Muestra esta ayuda
  /mode     - Explica los 3 modos de razonamiento
  /history  - Muestra el historial de la conversación
  /summary  - Muestra resumen de la sesión
  /export   - Exporta la conversación
  /reset    - Reinicia el agente (nueva sesión)
  /env      - Cambia el ambiente (dev/staging/prod)
  /quit     - Salir del programa
        """)
    
    elif command == '/mode':
        print("""
🧠 Los 3 Modos de Razonamiento de M.A.R.T.I.N.:

🟦 MODO PASIVO:
   • Se activa con: Tareas ambiguas o preguntas
   • Comportamiento: Propone plan y espera confirmación
   • Ejemplo: "Ayúdame con compliance"

🟩 MODO DIRECTO:
   • Se activa con: Tareas claras y seguras
   • Comportamiento: Ejecuta automáticamente
   • Ejemplo: "Genera política de contraseñas ISO 27001"

🟨 MODO SEGURO:
   • Se activa con: Acciones riesgosas o en producción
   • Comportamiento: Auto-valida antes de actuar
   • Ejemplo: "Eliminar base de datos"
        """)
    
    elif command == '/history':
        history = agent.get_conversation_history()
        if not history:
            print("📭 No hay historial aún")
        else:
            print("\n📜 Historial de conversación:")
            print("="*60)
            for i, item in enumerate(history):
                if item.get('input'):
                    print(f"\n[{i}] {item['timestamp']}")
                    print(f"Tu: {item['input'][:100]}...")
                    print(f"Modo: {item.get('mode_selected', 'N/A')}")
    
    elif command == '/summary':
        summary = agent.get_session_summary()
        print(f"""
📊 Resumen de la sesión:
   • Session ID: {summary['session_id']}
   • Interacciones: {summary['total_interactions']}
   • Modos usados: {summary.get('modes_distribution', {})}
        """)
    
    elif command == '/export':
        format_choice = input("Formato (json/text/markdown) [json]: ").strip() or 'json'
        if format_choice in ['json', 'text', 'markdown']:
            filename = f"martin_session_{agent.session_id}.{format_choice if format_choice != 'markdown' else 'md'}"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(agent.export_conversation(format_choice))
            print(f"✅ Conversación exportada a: {filename}")
        else:
            print("❌ Formato no válido")
    
    elif command == '/reset':
        confirm = input("¿Seguro que quieres reiniciar? Se perderá el historial (s/n): ")
        if confirm.lower() in ['s', 'si', 'sí', 'yes', 'y']:
            agent.reset()
            print("🔄 Agente reiniciado - Nueva sesión iniciada")
    
    elif command == '/env':
        print("\nCambiar ambiente:")
        print("1. Development")
        print("2. Staging")
        print("3. Production")
        env_choice = input("Selecciona (1-3): ").strip()
        
        new_env = {
            '1': 'development',
            '2': 'staging',
            '3': 'production'
        }.get(env_choice)
        
        if new_env:
            context['environment'] = new_env
            print(f"✅ Ambiente cambiado a: {new_env}")
            if new_env == 'production':
                print("⚠️  En producción, M.A.R.T.I.N. será más cauteloso")
        else:
            print("❌ Opción no válida")
    
    elif command in ['/quit', '/exit', '/q']:
        print("\n👋 ¡Hasta luego!")
        sys.exit(0)
    
    else:
        print(f"❌ Comando desconocido: {command}")
        print("Usa /help para ver los comandos disponibles")

def print_response(result: dict):
    """Imprime la respuesta de M.A.R.T.I.N. de forma bonita"""
    mode_emoji = {
        'PASSIVE': '🟦',
        'DIRECT': '🟩',
        'SAFE': '🟨'
    }.get(result.get('mode', ''), '⚪')
    
    print(f"\n{mode_emoji} M.A.R.T.I.N. ({result.get('mode', 'UNKNOWN')}):")
    print("-"*60)
    
    # Mostrar el mensaje principal
    message = result.get('message', result.get('results', 'Sin respuesta'))
    print(message)
    
    # Si está bloqueado, mostrar advertencia especial
    if result.get('status') == 'blocked':
        print("\n⚠️ ACCIÓN BLOQUEADA POR SEGURIDAD")
        if result.get('alternative_suggestion'):
            print("\n💡 Alternativa sugerida:")
            print(result['alternative_suggestion'])
    
    print("-"*60)

def main():
    """Función principal con argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description='M.A.R.T.I.N. - Agente de IA con razonamiento adaptativo'
    )
    
    parser.add_argument(
        '--mode',
        choices=['cli', 'web', 'test'],
        default='cli',
        help='Modo de ejecución (default: cli)'
    )
    
    parser.add_argument(
        '--llm',
        action='store_true',
        help='Forzar uso de LLM aunque no haya API key'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Modo verbose (más información de debug)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'cli':
        run_cli_mode()
    elif args.mode == 'web':
        print("🚧 Interfaz web próximamente...")
        print("Por ahora, usa: python ui/gradio_interface.py")
    elif args.mode == 'test':
        from tests.test_martin_agent import main as run_tests
        run_tests()
    else:
        print(f"❌ Modo no reconocido: {args.mode}")
        sys.exit(1)

if __name__ == "__main__":
    main()