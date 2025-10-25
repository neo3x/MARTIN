# debug_gradio_detailed.py
import sys
print("🔍 Python executable:", sys.executable)
print("\n🔍 Python path:")
for i, p in enumerate(sys.path):
    print(f"  {i}: {p}")

print("\n🔍 Intentando importar gradio...")
import gradio
print(f"✅ Gradio file: {gradio.__file__}")
print(f"✅ Gradio version: {gradio.__version__}")
print(f"✅ Gradio dir: {dir(gradio)[:10]}...")  # Primeros 10 atributos

print("\n🔍 ¿Tiene Blocks?")
print(f"  hasattr(gradio, 'Blocks'): {hasattr(gradio, 'Blocks')}")

if hasattr(gradio, 'Blocks'):
    print("\n✅ Gradio.Blocks existe - Intentando crear uno...")
    try:
        with gradio.Blocks() as demo:
            gradio.Markdown("# Test")
        print("✅ Blocks funciona correctamente")
    except Exception as e:
        print(f"❌ Error creando Blocks: {e}")
else:
    print("\n❌ Gradio NO tiene Blocks")
    print(f"  Versión instalada: {gradio.__version__}")
    print(f"  Ubicación: {gradio.__file__}")
    print("\n  Esto indica que Python está importando un gradio incorrecto")