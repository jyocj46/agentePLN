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