import cx_Oracle

dsn = cx_Oracle.makedsn("localhost", 1521, service_name="xe")
conn = cx_Oracle.connect("C##AGENTE", "123456", dsn)  # Usa tus credenciales
cursor = conn.cursor()

cursor.execute("""
    SELECT owner, table_name 
    FROM all_tables 
    WHERE table_name = 'FALLAS_INFORMATICAS'
""")

resultados = cursor.fetchall()
print("Tablas encontradas:")
for owner, table in resultados:
    print(f"👉 Esquema: {owner}, Tabla: {table}")

cursor.close()
conn.close()