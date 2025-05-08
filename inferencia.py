from conexion import conectar_oracle
import cx_Oracle
from typing import Tuple, Optional

def buscar_solucion(palabras_clave: list) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Busca soluciones técnicas basadas en palabras clave con sistema de priorización.
    
    Args:
        palabras_clave: Lista de palabras clave extraídas del PLN
        
    Returns:
        Tupla con (síntoma, causa_probable, solución) o (None, None, None) si no hay resultados
    """
    conn = None
    cursor = None
    
    try:
        conn = conectar_oracle()
        if not conn:
            return None, None, None

        cursor = conn.cursor()
        
        # Construcción dinámica de la consulta con scoring
        query = """
            SELECT 
                SINTOMA, 
                CAUSA_PROBABLE, 
                SOLUCION,
                SUM(
                    CASE
                        WHEN LOWER(PALABRAS_CLAVE) LIKE '%' || :palabra || '%' THEN 3
                        WHEN LOWER(SINTOMA) LIKE '%' || :palabra || '%' THEN 2
                        WHEN LOWER(CAUSA_PROBABLE) LIKE '%' || :palabra || '%' THEN 1
                        ELSE 0
                    END
                ) AS RELEVANCIA
            FROM C##AGENTE.FALLAS_INFORMATICAS
            WHERE """
        
        # Condiciones para cada palabra clave
        condiciones = []
        params = {}
        
        for i, palabra in enumerate(palabras_clave):
            condiciones.append(f"(LOWER(PALABRAS_CLAVE) LIKE '%' || :p{i} || '%' OR "
                             f"LOWER(SINTOMA) LIKE '%' || :p{i} || '%' OR "
                             f"LOWER(CAUSA_PROBABLE) LIKE '%' || :p{i} || '%')")
            params[f"p{i}"] = palabra.lower()
            params["palabra"] = palabra.lower()  # Para el scoring

        query += " OR ".join(condiciones)
        query += " GROUP BY SINTOMA, CAUSA_PROBABLE, SOLUCION ORDER BY RELEVANCIA DESC FETCH FIRST 1 ROWS ONLY"

        # Ejecutar consulta
        cursor.execute(query, params)
        resultado = cursor.fetchone()

        if resultado:
            return resultado[0], resultado[1], resultado[2]  # Síntoma, Causa, Solución
        
        # Si no hay resultados, intentar con términos más generales
        return buscar_solucion_generica(palabras_clave, conn)
        
    except cx_Oracle.DatabaseError as e:
        print(f"🔴 Error de base de datos: {e}")
        return None, None, None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def buscar_solucion_generica(palabras_clave: list, conn: cx_Oracle.Connection) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Búsqueda secundaria con términos más generales cuando no hay coincidencia exacta.
    """
    try:
        cursor = conn.cursor()
        
        # Consulta genérica para problemas relacionados
        query = """
            SELECT SINTOMA, CAUSA_PROBABLE, SOLUCION
            FROM C##AGENTE.FALLAS_INFORMATICAS
            WHERE CATEGORIA = (
                SELECT CATEGORIA 
                FROM C##AGENTE.FALLAS_INFORMATICAS
                WHERE """
        
        condiciones = []
        params = {}
        for i, palabra in enumerate(palabras_clave):
            condiciones.append(f"LOWER(PALABRAS_CLAVE) LIKE '%' || :gp{i} || '%'")
            params[f"gp{i}"] = palabra.lower()

        query += " OR ".join(condiciones)
        query += " FETCH FIRST 1 ROWS ONLY) ORDER BY PRIORIDAD DESC FETCH FIRST 1 ROWS ONLY"

        cursor.execute(query, params)
        resultado = cursor.fetchone()
        
        return resultado if resultado else (None, None, None)
        
    except Exception as e:
        print(f"⚠️ Error en búsqueda genérica: {e}")
        return None, None, None