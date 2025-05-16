from utils import extraer_palabras_clave, respuesta_aleatoria, terminos_tecnicos , saludos_extendidos, saludos, agradecimientos, frases_amables, temas_tecnicos_generales
from inferencia import buscar_solucion

def asistente_tecnico():
    print(" Asistente Técnico: Hola, ¿qué problema presenta tu computadora?")

    tipo_equipo = "ambos"
    interaccion_amable = False

    while True:
        entrada = input("Usuario: ").strip()

        # Comando de salida
        if entrada.lower() in ["salir", "exit", "terminar"]:
            print(" Hasta luego. ¡Espero haberte ayudado!")
            break

        # Entrada vacía
        if not entrada:
            print("No escribiste nada. Por favor, describe el problema de tu computadora.\n")
            continue

        entrada_normalizada = entrada.lower()
        interaccion_amable = False

        # Agradecimientos
        if any(agradecimiento in entrada_normalizada for agradecimiento in agradecimientos):
            print("¡De nada! Si necesitas más ayuda, aquí estaré.\n")
            continue

        # Saludo extendido tipo "¿cómo estás?"
        if any(pregunta in entrada_normalizada for pregunta in saludos_extendidos):
            print("¡Muy bien, gracias por preguntar! ¿En qué puedo ayudarte con tu computadora?\n")
            continue

        # Saludo simple
        if any(saludo in entrada_normalizada for saludo in saludos):
            if entrada_normalizada.strip() in saludos:
                print("¡Hola! Soy tu asistente técnico. ¿Puedes contarme qué problema presenta tu equipo?\n")
                continue
            else:
                print("¡Hola! Veo que mencionaste algo más, vamos a revisarlo...\n")

        # Frase amable tipo "mira, necesito ayuda"
            if any(frase in entrada_normalizada for frase in frases_amables):
                print("¡Claro! ¿En qué te puedo ayudar exactamente?\n")
                # Detectamos si además hay palabras técnicas en el mismo mensaje
                si_frase_amable_con_tecnica = any(t in entrada_normalizada for t in terminos_tecnicos)

                if not si_frase_amable_con_tecnica:
                    continue  # Solo detenemos si NO hay intención técnica

        # Detectar tipo de equipo si aún no se ha definido
        if tipo_equipo is None:
            texto = entrada_normalizada
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
                    print("No entendí el tipo de equipo. Por favor responde con 'laptop' o 'PC de escritorio'.\n")
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
            es_entrada_tecnica = any(t in entrada_normalizada for t in terminos_tecnicos + temas_tecnicos_generales)

            if es_entrada_tecnica:
                print("Hmm... no tengo registrada esta falla aún. ")
                print("¿Te gustaría enseñarme? Puedo aprender para ayudar a otros en el futuro.")

                confirmacion = input("¿Deseas agregar esta nueva falla? (sí/no): ").strip().lower()
                if confirmacion in ["sí", "si"]:
                    nuevo_sintoma = entrada.strip()
                    nueva_causa = input("¿Cuál fue la causa probable?: ").strip()
                    nueva_solucion = input("¿Cuál fue la solución que funcionó?: ").strip()
                    palabras_clave_extraidas = extraer_palabras_clave(nuevo_sintoma)
                    palabras_clave_str = ", ".join(palabras_clave_extraidas)

                    # Confirmar o pedir tipo de equipo
                    if tipo_equipo is None:
                        tipo_equipo = input("¿Es una laptop, una PC de escritorio o ambos?: ").strip().lower()
                        if tipo_equipo not in ["laptop", "escritorio", "ambos"]:
                            tipo_equipo = "ambos"

                    from conexion import conectar_oracle
                    conn = conectar_oracle()
                    if conn:
                        try:
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO C##AGENTE.FALLAS_INFORMATICAS (
                                    CATEGORIA, SUBCATEGORIA, SINTOMA, CAUSA_PROBABLE, SOLUCION,
                                    PALABRAS_CLAVE, TIPO_EQUIPO, PRIORIDAD
                                ) VALUES (
                                    :categoria, :subcategoria, :sintoma, :causa, :solucion,
                                    :palabras, :tipo, :prioridad
                                )
                            """, {
                                "categoria": "aprendido",
                                "subcategoria": "general",
                                "sintoma": nuevo_sintoma,
                                "causa": nueva_causa,
                                "solucion": nueva_solucion,
                                "palabras": palabras_clave_str,
                                "tipo": tipo_equipo,
                                "prioridad": 3
                            })
                            conn.commit()
                            print("✅ ¡Gracias! He aprendido esta nueva falla.\n")
                        except Exception as e:
                            print(f"❌ Error al guardar en la base de datos: {e}")
                        finally:
                            cursor.close()
                            conn.close()
                    else:
                        print("❌ No se pudo conectar a la base de datos para guardar la nueva falla.\n")
                else:
                    print("Está bien, si cambias de opinión me puedes enseñar más adelante.\n")
            else:
                print(respuesta_aleatoria())



# Ejecutar el programa
if __name__ == "__main__":
    asistente_tecnico()
