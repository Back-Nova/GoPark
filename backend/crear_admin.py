import bcrypt
from conexion import get_connection

# Datos del rol admin
rol_nombre = "admin"
rol_permisos = "todos"  # O los permisos que desees

# Datos del usuario admin
nombre = "admin"
apellido = "admin"
email = "santiagogokuaban@gmail.com"
password_plano = "admin"

# Hashear la contraseña
password_bytes = password_plano.encode('utf-8')
hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

# Conectar a la base de datos
conn = get_connection()
if conn is None:
    print("No se pudo conectar a la base de datos.")
    exit()

try:
    cur = conn.cursor()

    # Verificar si existe el rol admin
    cur.execute("SELECT id_rol FROM rol WHERE tipo_rol = %s", (rol_nombre,))
    rol_existente = cur.fetchone()

    if rol_existente:
        id_rol = rol_existente[0]
        print(f"El rol 'admin' ya existe con id {id_rol}.")
    else:
        cur.execute(
            "INSERT INTO rol (tipo_rol, permisos_rol) VALUES (%s, %s) RETURNING id_rol",
            (rol_nombre, rol_permisos)
        )
        id_rol = cur.fetchone()[0]
        print(f"Rol 'admin' creado con id {id_rol}.")

    # Verificar si ya existe el usuario
    cur.execute("SELECT id_usuario FROM usuario WHERE email = %s", (email,))
    usuario_existente = cur.fetchone()

    if usuario_existente:
        print("El usuario con este email ya existe.")
    else:
        # Insertar el usuario admin - CORREGIDO: usar id_rol en lugar de rol
        cur.execute("""
            INSERT INTO usuario (nombre, apellido, email, contraseña, id_rol)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellido, email, hashed_password.decode('utf-8'), id_rol))
        print("Usuario administrador creado correctamente.")

    conn.commit()
    cur.close()

except Exception as e:
    print("Error al crear el usuario:", e)

finally:
    conn.close()