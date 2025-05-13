import re
import spacy

# Cargar el modelo de spaCy en español
nlp_spacy = spacy.load("es_core_news_sm")

# Diccionario de sinónimos y errores comunes
sinonimos = {
    "compu": "computadora",
    "computardora": "computadora",
    "computadoratardoro": "computadora",
    "pc": "computadora",
    "ordenador": "computadora",
    "notebook": "computadora",
    "pantaya": "pantalla",
    "no jala": "no enciende",
    "no prende": "no enciende",
    "no arranca": "no enciende",
    "no junde": "no enciende",
    "no prende la compu": "no enciende computadora",
    "mira mi compu": "",
    "no se escucha": "sin sonido",
    "no hay red": "sin internet",
    "no funciona": "no enciende",
    "pantalla oscura": "pantalla negra",
    "pantalla apagada": "pantalla negra",
    "bsod": "pantalla azul",
    "kernel panic": "pantalla azul",
    "ralentizada": "lenta",
    "se traba": "lenta",
    "se congela": "lenta",
    "se apaga": "apagada",
    "bug": "error",
    "corrupto": "dañado"
}

def normalizar_texto(texto):
    texto = texto.lower()
    for original, reemplazo in sinonimos.items():
        texto = texto.replace(original, reemplazo)
    return texto

def extraer_palabras_clave(texto_usuario):
    texto_usuario = normalizar_texto(texto_usuario)
    doc = nlp_spacy(texto_usuario)
    palabras_clave = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return palabras_clave
