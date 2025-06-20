import psycopg2

# Función para conectarse a Railway
def get_connection():
    try:
        connection = psycopg2.connect(
            host='nozomi.proxy.rlwy.net',
            port=58285,
            database='railway',
            user='postgres',
            password='ehYRkTDLQdFMkqUdZDDmQZIEjlEPeBKE'
        )
        print("✅ Conexión exitosa a Railway.")
        return connection
    except Exception as e:
        print("❌ Error al conectar a la base de datos:", e)
        return None

# Función para ejecutar el script SQL
def ejecutar_script_sql(path_script):
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                with open(path_script, 'r', encoding='utf-8') as f:
                    sql = f.read()
                    cur.execute(sql)
                conn.commit()
                print("✅ Estructura de la base de datos creada o verificada correctamente.")
        except Exception as e:
            print("❌ Error al ejecutar el script SQL:", e)
            conn.rollback()
        finally:
            conn.close()
            print("🔒 Conexión cerrada.")

# Ejecutar solo si se llama directamente el script
if __name__ == '__main__':
    ejecutar_script_sql('GoPark_V2.sql')  # Asegúrate de que este archivo esté en la misma carpeta
