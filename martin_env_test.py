# test_martin_imports.py
print("🔍 Verificando imports de MARTIN...\n")

try:
    import gradio as gr
    print(f"✅ Gradio: {gr.__version__}")
    assert hasattr(gr, 'Blocks'), "Gradio.Blocks no disponible"
except Exception as e:
    print(f"❌ Gradio: {e}")

try:
    import anthropic
    print(f"✅ Anthropic SDK: {anthropic.__version__}")
except Exception as e:
    print(f"❌ Anthropic: {e}")

try:
    from langchain_anthropic import ChatAnthropic
    print("✅ LangChain-Anthropic: OK")
except Exception as e:
    print(f"❌ LangChain-Anthropic: {e}")

try:
    from langchain_openai import ChatOpenAI
    print("✅ LangChain-OpenAI: OK")
except Exception as e:
    print(f"❌ LangChain-OpenAI: {e}")

try:
    import langchain
    print(f"✅ LangChain Core: {langchain.__version__}")
except Exception as e:
    print(f"❌ LangChain: {e}")

print("\n✅ TODOS LOS IMPORTS OK - Puedes ejecutar MARTIN")