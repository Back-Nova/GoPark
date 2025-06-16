import psycopg2
def get_connection():
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='GoPark_V2',  # Nombre de tu base de datos
            user='postgres',
            password='Aban12062007'  # Cambia esto
        )
        return connection
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

print(get_connection)