# test_import_final.py
import sys
import gradio

print(f"Gradio location: {gradio.__file__}")
print(f"Debe estar en site-packages, NO en interface/")
print(f"Tiene Blocks: {hasattr(gradio, 'Blocks')}")
