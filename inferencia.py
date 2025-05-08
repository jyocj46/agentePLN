from conexion import conectar_oracle

def buscar_solucion(palabras_clave):
    conn = conectar_oracle()
    cursor = conn.cursor()

    query = "SELECT SINTOMA, CAUSA_PROBABLE, SOLUCION FROM FALLAS_INFORMATICAS WHERE "
    condiciones = []

    for palabra in palabras_clave:
        condiciones.append(f" LOWER(PALABRAS_CLAVE) LIKE '%{palabra.lower()}%' ")

    query += " OR ".join(condiciones)

    cursor.execute(query)
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    if resultado:
        return resultado
    else:
        return None, None, None
 