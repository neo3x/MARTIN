"""
Interfaz de usuario con Gradio para M.A.R.T.I.N.
Con soporte para múltiples LLMs (OpenAI y Claude)
"""
import sys
import os
from pathlib import Path

# Agregar directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

import gradio as gr
from agent_core.martin_agent import MARTINAgent
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class MARTINInterface:
    def __init__(self, llm_provider="auto"):
        """
        Args:
            llm_provider: "openai", "claude", o "auto"
        """
        # Detectar API keys disponibles
        self.has_openai = os.getenv('OPENAI_API_KEY') is not None
        self.has_claude = os.getenv('ANTHROPIC_API_KEY') is not None
        
        use_llm = self.has_openai or self.has_claude
        
        self.agent = MARTINAgent(
            use_llm=use_llm,
            llm_provider=llm_provider,
            verbose=False
        )
        self.conversation = []
        
        # Mostrar estado inicial
        if use_llm:
            if self.agent.llm_provider == "openai":
                print("✅ Usando OpenAI GPT-4")
            elif self.agent.llm_provider == "claude":
                print("✅ Usando Anthropic Claude 3.5 Sonnet")
        else:
            print("⚠️  Sin API Keys - Usando modo simulado")
            print("   Para usar LLMs reales, configura API keys en .env")
    
    def switch_llm(self, provider):
        """Cambia el proveedor de LLM"""
        
        # Verificar que tenga la API key necesaria
        if provider == "openai" and not self.has_openai:
            return "❌ OPENAI_API_KEY no configurada en .env"
        
        if provider == "claude" and not self.has_claude:
            return "❌ ANTHROPIC_API_KEY no configurada en .env"
        
        # Reiniciar agente con nuevo proveedor
        self.agent = MARTINAgent(
            use_llm=True,
            llm_provider=provider,
            verbose=False
        )
        
        provider_names = {
            "openai": "OpenAI GPT-4",
            "claude": "Anthropic Claude 3.5 Sonnet"
        }
        
        return f"✅ Cambiado a {provider_names.get(provider, provider)}"
    
    def process_message(self, message, environment, history):
        """Procesa mensaje del usuario"""
        
        if not message.strip():
            return history, "", "Por favor ingresa un mensaje"
        
        context = {
            'environment': environment
        }
        
        # Procesar con M.A.R.T.I.N.
        result = self.agent.process(message, context)
        
        # Formatear respuesta
        response = self._format_response(result)
        mode_info = self._format_mode_info(result)
        
        # Agregar a historial
        history.append((message, response))
        
        return history, "", mode_info
    
    def _format_response(self, result):
        """Formatea la respuesta de M.A.R.T.I.N. para mostrar en UI"""
        
        mode_emoji = {
            'PASSIVE': '🟦',
            'DIRECT': '🟩',
            'SAFE': '🟨'
        }
        
        emoji = mode_emoji.get(result['mode'], '⚪')
        
        response = f"{emoji} **Modo {result['mode']} activado**\n\n"
        response += result['message']
        
        if result.get('requires_user_action'):
            response += "\n\n⚠️ *Esperando tu confirmación para continuar*"
        
        return response
    
    def _format_mode_info(self, result):
        """Muestra información sobre por qué se eligió ese modo"""
        return result.get('mode_explanation', 'No hay explicación disponible')
    
    def reset_conversation(self):
        """Reinicia la conversación"""
        self.agent.reset()
        return [], "✅ Conversación reiniciada"
    
    def export_conversation(self):
        """Exporta la conversación"""
        filepath = self.agent.export_conversation()
        return f"✅ Conversación exportada a: {filepath}"
    
    def get_stats(self):
        """Obtiene estadísticas"""
        stats = self.agent.get_stats()
        llm_info = {
            "openai": "OpenAI GPT-4",
            "claude": "Anthropic Claude 3.5 Sonnet",
            "simulado": "Modo simulado (sin API key)"
        }.get(stats['llm_provider'], stats['llm_provider'])
        
        return f"""
📊 ESTADÍSTICAS DE LA SESIÓN

Total de interacciones: {stats['total_interactions']}
Modos usados: {stats['modes_used']}
Session ID: {stats['session_id']}
LLM: {llm_info}
"""
    
    def create_interface(self):
        """Crea la interfaz Gradio con selector de LLM"""
        
        with gr.Blocks(
            title="M.A.R.T.I.N. Agent",
            theme=gr.themes.Soft()
        ) as interface:
            
            gr.Markdown("""
            # 🧠 M.A.R.T.I.N.
            ## Modular Assistant for Reasoning, Tactics, Inference and Navigation
            
            Agente de IA con **razonamiento tri-modal adaptativo** para compliance automation
            """)
            
            # Selector de LLM (solo si hay al menos una API key)
            if self.has_openai or self.has_claude:
                with gr.Row():
                    gr.Markdown("### 🤖 Seleccionar LLM:")
                    
                    llm_choices = []
                    if self.has_openai:
                        llm_choices.append(("GPT-4 (OpenAI)", "openai"))
                    if self.has_claude:
                        llm_choices.append(("Claude 3.5 (Anthropic)", "claude"))
                    
                    llm_selector = gr.Radio(
                        choices=llm_choices,
                        value=llm_choices[0][1] if llm_choices else None,
                        label="Proveedor de LLM",
                        info="Puedes cambiar entre modelos durante la conversación"
                    )
                    
                    current_llm = "GPT-4" if self.agent.llm_provider == "openai" else "Claude 3.5" if self.agent.llm_provider == "claude" else "Simulado"
                    
                    llm_status = gr.Textbox(
                        label="Estado actual",
                        value=f"✅ Usando {current_llm}",
                        interactive=False,
                        lines=1
                    )
            else:
                gr.Markdown("""
                ⚠️ **Sin API Keys configuradas** - Ejecutando en modo simulado
                
                Para usar LLMs reales:
                1. Copia `.env.example` a `.env`
                2. Agrega tu `OPENAI_API_KEY` o `ANTHROPIC_API_KEY`
                3. Reinicia la aplicación
                """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(
                        label="Conversación con M.A.R.T.I.N.",
                        height=500,
                        show_label=True
                    )
                    
                    with gr.Row():
                        msg_input = gr.Textbox(
                            label="Tu mensaje",
                            placeholder="Ej: Ayúdame a preparar mi startup para SOC 2",
                            lines=2,
                            show_label=False
                        )
                    
                    with gr.Row():
                        submit_btn = gr.Button("Enviar", variant="primary", scale=2)
                        clear_btn = gr.Button("Limpiar", scale=1)
                    
                    with gr.Row():
                        environment = gr.Radio(
                            choices=["development", "staging", "production"],
                            value="development",
                            label="🌍 Ambiente",
                            info="El ambiente afecta cómo M.A.R.T.I.N. razona"
                        )
                
                with gr.Column(scale=1):
                    mode_info = gr.Textbox(
                        label="🧠 Razonamiento de M.A.R.T.I.N.",
                        lines=15,
                        max_lines=25,
                        show_label=True,
                        interactive=False
                    )
                    
                    gr.Markdown("""
                    ### Modos de Razonamiento:
                    
                    🟦 **PASIVO**: Propone plan, espera confirmación  
                    *Uso: Tareas ambiguas, exploración*
                    
                    🟩 **DIRECTO**: Ejecuta autónomamente  
                    *Uso: Tareas claras, bajo riesgo*
                    
                    🟨 **SEGURO**: Auto-valida antes de actuar  
                    *Uso: Alto riesgo, producción*
                    """)
                    
                    with gr.Row():
                        export_btn = gr.Button("📁 Exportar", scale=1)
                        stats_btn = gr.Button("📊 Stats", scale=1)
                    
                    output_info = gr.Textbox(
                        label="Información",
                        lines=4,
                        show_label=False,
                        interactive=False
                    )
            
            gr.Markdown("""
            ---
            ### 💡 Ejemplos de queries:
            
            **Modo Pasivo:**
            - "Ayúdame a preparar compliance para SOC 2"
            - "¿Cómo configuro mi firewall para seguridad?"
            
            **Modo Directo:**
            - "Genera política de contraseñas según ISO 27001"
            - "Crea un checklist de onboarding de empleados"
            
            **Modo Seguro:**
            - "Deshabilita usuario admin@empresa.com" (en producción)
            - "Elimina todos los logs antiguos"
            """)
            
            # Event handlers
            def submit(message, env, history):
                new_history, cleared_input, mode_explanation = self.process_message(
                    message, env, history
                )
                return new_history, cleared_input, mode_explanation
            
            submit_btn.click(
                submit,
                inputs=[msg_input, environment, chatbot],
                outputs=[chatbot, msg_input, mode_info]
            )
            
            msg_input.submit(
                submit,
                inputs=[msg_input, environment, chatbot],
                outputs=[chatbot, msg_input, mode_info]
            )
            
            clear_btn.click(
                lambda: self.reset_conversation(),
                outputs=[chatbot, output_info]
            )
            
            export_btn.click(
                lambda: self.export_conversation(),
                outputs=[output_info]
            )
            
            stats_btn.click(
                lambda: self.get_stats(),
                outputs=[output_info]
            )
            
            # Event handler para cambio de LLM
            if self.has_openai or self.has_claude:
                llm_selector.change(
                    self.switch_llm,
                    inputs=[llm_selector],
                    outputs=[llm_status]
                )
        
        return interface


def main():
    """Función principal"""
    print("="*60)
    print("🧠 M.A.R.T.I.N. - Interfaz Gradio")
    print("="*60)
    
    # Detectar LLM provider desde .env o auto
    llm_provider = os.getenv('LLM_PROVIDER', 'auto')
    
    ui = MARTINInterface(llm_provider=llm_provider)
    interface = ui.create_interface()
    
    print("\n🚀 Lanzando interfaz web...")
    print("📍 Una vez iniciada, abre el navegador en la URL que aparece")
    
    if ui.has_openai or ui.has_claude:
        print("\n✅ API Keys detectadas:")
        if ui.has_openai:
            print("   • OpenAI GPT-4")
        if ui.has_claude:
            print("   • Anthropic Claude 3.5 Sonnet")
        print("\n💡 Puedes cambiar entre modelos desde la interfaz")
    else:
        print("\n⚠️  Ejecutando en modo simulado")
        print("   Para usar LLMs reales, configura tu API key en .env")
    
    print()
    
    interface.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860
    )


if __name__ == "__main__":
    main()