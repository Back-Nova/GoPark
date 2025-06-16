BEGIN;

-- Tabla ROL
CREATE TABLE IF NOT EXISTS public.rol (
    id_rol serial PRIMARY KEY,
    tipo_rol varchar(50),
    permisos_rol varchar(255)
);

-- Tabla USUARIO
CREATE TABLE IF NOT EXISTS public.usuario (
    id_usuario serial PRIMARY KEY,
    nombre varchar(100),
    apellido varchar(100),
    email varchar(150),
    contraseña varchar(100),
    id_rol integer,
    CONSTRAINT fk_usuario_rol FOREIGN KEY (id_rol) REFERENCES public.rol (id_rol)
);

-- Tabla DESTINO
CREATE TABLE IF NOT EXISTS public.destino (
    id_destino serial PRIMARY KEY,
    pais varchar(50),
    ciudad varchar(100),
    region varchar(100),
    descripcion text
);

-- Tabla ALOJAMIENTO
CREATE TABLE IF NOT EXISTS public.alojamiento (
    id_alojamiento serial PRIMARY KEY,
    nombre varchar(100),
    descripcion varchar(255),
    tipo_alojamiento varchar(50),
    capacidad integer,
    precio numeric(10,2),
    destino integer,
    CONSTRAINT fk_alojamiento_destino FOREIGN KEY (destino) REFERENCES public.destino (id_destino)
);

-- Tabla VEHICULO ALQUILER
CREATE TABLE IF NOT EXISTS public.vehiculo_alquiler (
    id_vehiculo serial PRIMARY KEY,
    marca varchar(50),
    modelo varchar(50),
    capacidad integer,
    destino integer,
    CONSTRAINT fk_vehiculo_destino FOREIGN KEY (destino) REFERENCES public.destino (id_destino)
);

-- Tabla VUELO
CREATE TABLE IF NOT EXISTS public.vuelo (
    id_vuelo serial PRIMARY KEY,
    aerolinea varchar(100),
    aeropuerto_o varchar(100),
    aeropuerto_d varchar(100),
    fecha date,
    duracion varchar(50),
    precio numeric(10,2),
    destino integer,
    CONSTRAINT fk_vuelo_destino FOREIGN KEY (destino) REFERENCES public.destino (id_destino)
);

-- Tabla EXCURSION
CREATE TABLE IF NOT EXISTS public.excursion (
    id_excursion serial PRIMARY KEY,
    nombre varchar(100),
    descripcion varchar(255),
    duracion varchar(50),
    precio_adulto numeric(10,2),
    precio_nino numeric(10,2),
    participantes varchar(100),
    destino integer,
    CONSTRAINT fk_excursion_destino FOREIGN KEY (destino) REFERENCES public.destino (id_destino)
);

-- Tabla PAQUETE
CREATE TABLE IF NOT EXISTS public.paquete (
    id_paquete serial PRIMARY KEY,
    nombre varchar(100),
    descripcion varchar(255),
    precio numeric(10,2),
    cupos_totales integer,
    cupos_disponibles integer,
    fecha_inicio date,
    fecha_fin date,
    tipo varchar(50),
    disponible boolean,
    vuelo integer,
    vehiculo integer,
    alojamiento integer,
    excursion integer,
    CONSTRAINT fk_paquete_vuelo FOREIGN KEY (vuelo) REFERENCES public.vuelo (id_vuelo),
    CONSTRAINT fk_paquete_vehiculo FOREIGN KEY (vehiculo) REFERENCES public.vehiculo_alquiler (id_vehiculo),
    CONSTRAINT fk_paquete_alojamiento FOREIGN KEY (alojamiento) REFERENCES public.alojamiento (id_alojamiento),
    CONSTRAINT fk_paquete_excursion FOREIGN KEY (excursion) REFERENCES public.excursion (id_excursion)
);

-- Tabla RESERVA
CREATE TABLE IF NOT EXISTS public.reserva (
    id_reserva serial PRIMARY KEY,
    id_paquete integer,
    fecha_reserva date,
    cantidad_personas integer,
    id_usuario integer NOT NULL,
    estado boolean,
    observaciones text,
    CONSTRAINT fk_reserva_paquete FOREIGN KEY (id_paquete) REFERENCES public.paquete (id_paquete),
    CONSTRAINT fk_reserva_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuario (id_usuario)
);

-- Tabla CARRITO
CREATE TABLE IF NOT EXISTS public.carrito (
    id_carrito serial PRIMARY KEY,
    reserva integer NOT NULL,
    fecha_carrito date,
    precio_final numeric(10,2),
    metodo_pago varchar(50),
    estado_pago varchar(50),
    CONSTRAINT fk_carrito_reserva FOREIGN KEY (reserva) REFERENCES public.reserva (id_reserva)
);

-- Tabla VENTAS
CREATE TABLE IF NOT EXISTS public.ventas (
    id_venta serial PRIMARY KEY,
    id_reserva integer NOT NULL,
    fecha_entrega date,
    monto_cobrado numeric(10, 2),
    CONSTRAINT fk_ventas_reserva FOREIGN KEY (id_reserva) REFERENCES public.reserva (id_reserva)
);

-- Tabla RECUPERACION CUENTA
CREATE TABLE IF NOT EXISTS public.recuperacion_cuenta (
    id_restablecer serial PRIMARY KEY,
    codigo varchar(255),
    codigo_hash varchar(255),
    expiracion timestamp,
    usuario integer NOT NULL,
    CONSTRAINT fk_recuperacion_usuario FOREIGN KEY (usuario) REFERENCES public.usuario (id_usuario)
);

-- Tabla REPORTE
CREATE TABLE IF NOT EXISTS public.reporte (
    id_reporte serial PRIMARY KEY,
    id_usuario integer NOT NULL,
    tipo_reporte varchar(50),
    fecha_generacion date,
    contenido text,
    parametros text,
    CONSTRAINT fk_reporte_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuario (id_usuario)
);

-- Tabla SESION USUARIO
CREATE TABLE IF NOT EXISTS public.sesion_usuario (
    id_sesion serial PRIMARY KEY,
    fecha_sesion timestamp,
    ip_address varchar(50),
    sesion_activa boolean,
    id_usuario integer NOT NULL,
    CONSTRAINT fk_sesion_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuario (id_usuario)
);

END;
