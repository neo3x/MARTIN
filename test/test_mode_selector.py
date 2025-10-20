"""
Tests para validar que el ModeSelector elige correctamente
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_core.mode_selector import ModeSelector

def run_tests():
    """Ejecuta todos los tests del ModeSelector"""
    selector = ModeSelector()
    passed_tests = 0
    failed_tests = 0
    
    print("🧪 INICIANDO TESTS DEL MODE SELECTOR\n")
    print("="*60)
    
    # Lista de casos de prueba
    test_cases = [
        # TEST 1: Modo PASSIVE - Tarea ambigua
        {
            'name': 'Tarea ambigua',
            'input': 'Ayúdame con SOC 2',
            'context': {},
            'expected': 'PASSIVE',
            'reason': 'Solicitud vaga sin detalles específicos'
        },
        
        # TEST 2: Modo DIRECT - Tarea clara y segura
        {
            'name': 'Tarea clara y segura',
            'input': 'Genera una política de contraseñas según ISO 27001 para empresa de 50 empleados',
            'context': {},
            'expected': 'DIRECT',
            'reason': 'Instrucción específica sin riesgos'
        },
        
        # TEST 3: Modo SAFE - Acción peligrosa
        {
            'name': 'Acción peligrosa',
            'input': 'Delete all users from the production database',
            'context': {},
            'expected': 'SAFE',
            'reason': 'Contiene palabras peligrosas y recursos críticos'
        },
        
        # TEST 4: Modo SAFE - Producción
        {
            'name': 'Ambiente de producción',
            'input': 'Update configuration file',
            'context': {'environment': 'production'},
            'expected': 'SAFE',
            'reason': 'Cualquier acción en producción requiere validación'
        },
        
        # TEST 5: Modo PASSIVE - Pregunta
        {
            'name': 'Pregunta del usuario',
            'input': '¿Cómo configuro mi firewall para compliance?',
            'context': {},
            'expected': 'PASSIVE',
            'reason': 'Es una pregunta que requiere guía'
        },
        
        # TEST 6: Modo SAFE - Deshabilitar MFA admin
        {
            'name': 'Deshabilitar seguridad crítica',
            'input': 'Deshabilita la autenticación multifactor del usuario admin@empresa.com',
            'context': {'environment': 'staging'},
            'expected': 'SAFE',
            'reason': 'Acción que reduce seguridad en cuenta admin'
        },
        
        # TEST 7: Modo DIRECT - Escaneo read-only
        {
            'name': 'Escaneo de solo lectura',
            'input': 'Escanea mi organización de GitHub buscando problemas de compliance',
            'context': {'environment': 'development'},
            'expected': 'DIRECT',
            'reason': 'Operación de solo lectura sin riesgo'
        },
        
        # TEST 8: Modo PASSIVE - Solicitud genérica
        {
            'name': 'Solicitud muy genérica',
            'input': 'Compliance',
            'context': {},
            'expected': 'PASSIVE',
            'reason': 'Una sola palabra, demasiado vago'
        },
        
        # TEST 9: Modo SAFE - Eliminar todos los recursos
        {
            'name': 'Eliminación masiva',
            'input': 'Elimina todos los repositorios privados de la organización',
            'context': {},
            'expected': 'SAFE',
            'reason': 'Eliminar + todos = alto riesgo'
        },
        
        # TEST 10: Modo DIRECT - Generar reporte
        {
            'name': 'Generación de reporte',
            'input': 'Genera un reporte de gaps de compliance SOC 2 para TechStartup Inc',
            'context': {'environment': 'development'},
            'expected': 'DIRECT',
            'reason': 'Generación de documentación sin riesgo'
        }
    ]
    
    # Ejecutar cada test
    for i, test in enumerate(test_cases, 1):
        print(f"\n🧪 TEST {i}: {test['name']}")
        print("-" * 40)
        
        # Ejecutar selector
        mode = selector.select_mode(test['input'], test['context'])
        
        # Verificar resultado
        if mode == test['expected']:
            print(f"✅ PASSED - Modo esperado: {test['expected']}")
            print(f"   Razón del test: {test['reason']}")
            passed_tests += 1
        else:
            print(f"❌ FAILED - Esperado: {test['expected']}, Obtenido: {mode}")
            print(f"   Razón del test: {test['reason']}")
            failed_tests += 1
        
        # Mostrar explicación del selector
        print(selector.explain_last_decision())
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DE TESTS")
    print("="*60)
    print(f"✅ Tests pasados: {passed_tests}/{len(test_cases)}")
    print(f"❌ Tests fallados: {failed_tests}/{len(test_cases)}")
    
    # Estadísticas del selector
    stats = selector.get_statistics()
    print("\n📈 ESTADÍSTICAS DEL SELECTOR:")
    print(f"   Total de decisiones: {stats.get('total_decisions', 0)}")
    if 'modes_distribution' in stats:
        print(f"   Distribución de modos:")
        for mode, count in stats['modes_distribution'].items():
            emoji = {'PASSIVE': '🟦', 'DIRECT': '🟩', 'SAFE': '🟨'}.get(mode, '⚪')
            print(f"      {emoji} {mode}: {count}")
    print(f"   Promedio de riesgo: {stats.get('average_risk_score', 0)}")
    print(f"   Promedio de claridad: {stats.get('average_clarity_score', 0)}")
    
    if failed_tests == 0:
        print("\n🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
    else:
        print(f"\n⚠️ Hay {failed_tests} tests que necesitan revisión")
    
    return passed_tests == len(test_cases)

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)