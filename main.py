from utils import extraer_palabras_clave
from inferencia import buscar_solucion

def asistente_tecnico():
    print("👨‍💻 Asistente Técnico: Hola, ¿qué problema presenta tu computadora?")

    tipo_equipo = "ambos"
    saludos = ["hola", "buenos días", "buenas", "qué tal", "hey"]

    while True:
        entrada = input("Usuario: ").strip()

        # Comando de salida
        if entrada.lower() in ["salir", "exit", "terminar"]:
            print("👋 Hasta luego. ¡Espero haberte ayudado!")
            break

        # Entrada vacía
        if not entrada:
            print("No escribiste nada. Por favor, describe el problema de tu computadora.\n")
            continue

        # Saludo simple
        if entrada.lower() in saludos:
            print("👋 ¡Hola! Soy tu asistente técnico. ¿Puedes contarme qué problema presenta tu equipo?\n")
            continue

        # Detectar tipo de equipo si aún no se ha definido
        if tipo_equipo is None:
            texto = entrada.lower()
            if any(palabra in texto for palabra in ["laptop", "portátil", "notebook"]):
                tipo_equipo = "laptop"
                print("Entendido, estás usando una laptop.\n")
            elif any(palabra in texto for palabra in ["pc", "escritorio", "computadora de escritorio"]):
                tipo_equipo = "escritorio"
                print("Entendido, estás usando una computadora de escritorio.\n")
            else:
                print("Antes de continuar, ¿estás usando una laptop o una computadora de escritorio?")
                respuesta = input("Usuario: ").strip().lower()
                if "laptop" in respuesta or "portátil" in respuesta or "notebook" in respuesta:
                    tipo_equipo = "laptop"
                elif "pc" in respuesta or "escritorio" in respuesta:
                    tipo_equipo = "escritorio"
                else:
                    print("❗ No entendí el tipo de equipo. Por favor responde con 'laptop' o 'PC de escritorio'.\n")
                    continue
                print(f" Gracias. Notado: estás usando una {tipo_equipo}.\n")

        # Procesar entrada
        palabras_clave = extraer_palabras_clave(entrada)
        print(f"Palabras clave detectadas: {palabras_clave}")

        sintoma, causa, solucion = buscar_solucion(palabras_clave, tipo_equipo)

        if sintoma:
            # Adaptar la solución si aplica
            if tipo_equipo == "laptop" and "tarjeta gráfica" in solucion.lower():
                solucion += " (Nota: En laptops, cambiar la tarjeta gráfica no siempre es posible. Considera asistencia técnica especializada.)"

            print(f"\nDiagnóstico: {sintoma}")
            print(f"Causa probable: {causa}")
            print(f"Solución sugerida: {solucion}\n")
        else:
            print("No logré entender bien el problema...")
            print("¿Podrías describirlo con más detalle o de otra manera?")
            print("Ejemplos: 'Mi computadora no enciende', 'No tengo internet', 'Pantalla negra', etc.\n")

# Ejecutar el programa
if __name__ == "__main__":
    asistente_tecnico()
