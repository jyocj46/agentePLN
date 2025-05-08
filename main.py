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
