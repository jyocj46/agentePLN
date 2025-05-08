import cx_Oracle

dsn = cx_Oracle.makedsn("localhost", 1521, service_name="xepdb1")
conn = cx_Oracle.connect("C##AGENTE", "123456", dsn)
cursor = conn.cursor()

try:
    # Verifica usuario conectado
    cursor.execute("SELECT username FROM user_users")
    print("👤 Usuario conectado:", cursor.fetchone()[0])

    # Verifica PDB
    cursor.execute("SELECT sys_context('userenv', 'con_name') FROM dual")
    print("📦 PDB conectado:", cursor.fetchone()[0])

    # Verifica si la tabla es accesible
    cursor.execute("SELECT COUNT(*) FROM FALLAS_INFORMATICAS")
    print("✅ Tabla accesible, total registros:", cursor.fetchone()[0])

except cx_Oracle.DatabaseError as e:
    print("❌ Error de base de datos:", e)

finally:
    cursor.close()
    conn.close()
