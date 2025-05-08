import re

def extraer_palabras_clave(texto_usuario):
    texto_usuario = texto_usuario.lower()
    palabras = re.findall(r'\b\w+\b', texto_usuario)
    return palabras
