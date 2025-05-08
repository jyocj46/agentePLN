conexion.py
import cx_Oracle
from typing import Optional

def conectar_oracle() -> Optional[cx_Oracle.Connection]:
    try:
        dsn = cx_Oracle.makedsn(
            host="localhost",
            port=1521,
            service_name="xe"
        )
        
        # Conexión normal sin SYSDBA
        conn = cx_Oracle.connect(
            user="C##AGENTE",
            password="123456",
            dsn=dsn,
            encoding="UTF-8"
        )
        
        # Verificar conexión
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM DUAL")
            if cursor.fetchone()[0] != 1:
                raise cx_Oracle.DatabaseError("Verificación de conexión fallida")
        
        print("✅ Conexión exitosa a Oracle")
        return conn
        
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"❌ Error Oracle (Code: {error.code}):")
        print(f"Message: {error.message}")
        print(f"Context: {error.context}")
        print("Solución: Verificar privilegios con 'GRANT CREATE SESSION TO C##AGENTE'")
        return None
--------------------------------------------------
inferencia.py
from conexion import conectar_oracle
import cx_Oracle  # ¡Añade esta línea para manejar excepciones!

def buscar_solucion(palabras_clave):
    conn = None
    cursor = None
    try:
        conn = conectar_oracle()
        cursor = conn.cursor()
        
        # Usa el nombre completo del esquema (C##AGENTE.)
        query = """
            SELECT SINTOMA, CAUSA_PROBABLE, SOLUCION 
            FROM C##AGENTE.FALLAS_INFORMATICAS 
            WHERE """
        
        condiciones = []
        params = []
        for i, palabra in enumerate(palabras_clave, 1):
            condiciones.append(f"LOWER(PALABRAS_CLAVE) LIKE '%' || :{i} || '%'")
            params.append(palabra.lower())
        
        query += " OR ".join(condiciones)
        cursor.execute(query, params)
        
        resultado = cursor.fetchone()
        return resultado if resultado else (None, None, None)
        
    except cx_Oracle.DatabaseError as e:
        print(f"🔴 Error de base de datos: {e}")
        return None, None, None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

-----------------------------------------
main.py 

from utils import extraer_palabras_clave
from inferencia import buscar_solucion


def asistente_tecnico():
    print("👨‍💻 Asistente Técnico: Hola, ¿qué problema presenta tu computadora?")
    
    while True:
        entrada = input("Usuario: ")
        if entrada.lower() in ["salir", "exit", "terminar"]:
            print("👋 Hasta luego.")
            break

        palabras_clave = extraer_palabras_clave(entrada)
        print(f"🔎 Palabras clave detectadas: {palabras_clave}")  # Opcional: para depurar

        sintoma, causa, solucion = buscar_solucion(palabras_clave)
        
        if sintoma:
            print(f"\n🔍 Diagnóstico: {sintoma}")
            print(f"🧠 Causa probable: {causa}")
            print(f"🛠️ Solución sugerida: {solucion}\n")
        else:
            print("❌ Lo siento, no encontré una solución. Intenta describir el problema de otra forma.\n")

# Ejecutar el programa
if __name__ == "__main__":
    asistente_tecnico()
---------------------------------------------------
utils.py

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
    "se traba": "lenta"
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
--------------------------------------------
pln.py 

import re

def extraer_palabras_clave(texto_usuario):
    texto_usuario = texto_usuario.lower()
    palabras = re.findall(r'\b\w+\b', texto_usuario)
    return palabras

