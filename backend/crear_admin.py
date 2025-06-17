from werkzeug.security import generate_password_hash
from conexion import get_connection

# Datos del usuario admin
nombre = "admin"
apellido = "admin"
email = "Prueba@gmail.com"
password_plano = "admin"

# Hashear la contraseña usando werkzeug (compatible con tu login)
hashed_password = generate_password_hash(password_plano)

# Conectar a la base de datos
conn = get_connection()
if conn is None:
    print("No se pudo conectar a la base de datos.")
    exit()

try:
    cur = conn.cursor()

    # Verificar si existe el rol admin
    cur.execute("SELECT id_rol FROM rol WHERE tipo_rol = %s", ("admin",))
    rol_existente = cur.fetchone()

    if rol_existente:
        id_rol = rol_existente[0]
        print(f"El rol 'admin' ya existe con id {id_rol}.")
    else:
        cur.execute(
            "INSERT INTO rol (tipo_rol, permisos_rol) VALUES (%s, %s) RETURNING id_rol",
            ("admin", "todos")
        )
        id_rol = cur.fetchone()[0]
        print(f"Rol 'admin' creado con id {id_rol}.")

    # Verificar si ya existe el usuario
    cur.execute("SELECT id_usuario FROM usuario WHERE email = %s", (email,))
    usuario_existente = cur.fetchone()

    if usuario_existente:
        print("El usuario con este email ya existe.")
    else:
        cur.execute("""
            INSERT INTO usuario (nombre, apellido, email, contraseña, id_rol)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellido, email, hashed_password, id_rol))
        print("Usuario administrador creado correctamente.")

    conn.commit()
    cur.close()

except Exception as e:
    print("Error al crear el usuario:", e)

finally:
    conn.close()