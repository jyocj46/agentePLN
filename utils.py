import re
from textblob import TextBlob
import spacy

# Cargamos el modelo en español
nlp_spacy = spacy.load("es_core_news_sm")

# Diccionario de sinónimos y normalización semántica
sinonimos = {
    "compu": "computadora",
    "pc": "computadora",
    "ordenador": "computadora",
    "laptop": "computadora",
    "notebook": "computadora",
    "no jala": "no funciona",
    "no junde": "no funciona",
    "bug": "error",
    "pantalla oscura": "pantalla negra",
    "ralentizada": "lenta",
    "se apaga": "apagada",
    "no prende": "no enciende",
    "no arranca": "no enciende",
    "no prende la compu": "no enciende computadora",
    "sin red": "sin internet",
    "se congela": "lenta",
    "no se escucha": "sin sonido",
    "se traba": "lenta",
    "bsod": "pantalla azul",
    "kernel panic": "error grave",
    "corrupto": "dañado"
}

def corregir_ortografia(texto):
    excepciones = ["pantalla", "wifi", "laptop", "compu", "router"]
    palabras = texto.split()
    texto_corregido = []

    for palabra in palabras:
        if palabra.lower() in excepciones:
            texto_corregido.append(palabra)
        else:
            texto_corregido.append(str(TextBlob(palabra).correct()))

    return " ".join(texto_corregido)

def normalizar_texto(texto):
    texto = texto.lower()
    for original, reemplazo in sinonimos.items():
        texto = texto.replace(original, reemplazo)
    return texto

def extraer_palabras_clave(texto_usuario):
    texto_usuario = corregir_ortografia(texto_usuario)
    texto_usuario = normalizar_texto(texto_usuario)
    doc = nlp_spacy(texto_usuario)
    palabras_clave = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return palabras_clave
