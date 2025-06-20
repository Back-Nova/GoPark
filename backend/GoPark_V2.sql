BEGIN;


CREATE TABLE IF NOT EXISTS public.excursion
(
    id_excursion serial NOT NULL,
    nombre character varying(100) COLLATE pg_catalog."default",
    descripcion character varying(255) COLLATE pg_catalog."default",
    duracion character varying(50) COLLATE pg_catalog."default",
    precio_adulto numeric(10, 2),
    precio_nino numeric(10, 2),
    participantes character varying(100) COLLATE pg_catalog."default",
    destino integer,
    CONSTRAINT excursion_pkey PRIMARY KEY (id_excursion)
);

CREATE TABLE IF NOT EXISTS public.destino
(
    id_destino serial NOT NULL,
    pais character varying(50) COLLATE pg_catalog."default",
    ciudad character varying(100) COLLATE pg_catalog."default",
    region character varying(100) COLLATE pg_catalog."default",
    descripcion text COLLATE pg_catalog."default",
    CONSTRAINT destino_pkey PRIMARY KEY (id_destino)
);

CREATE TABLE IF NOT EXISTS public.alojamiento
(
    id_alojamiento serial NOT NULL,
    nombre character varying(100) COLLATE pg_catalog."default",
    descripcion character varying(255) COLLATE pg_catalog."default",
    tipo_alojamiento character varying(50) COLLATE pg_catalog."default",
    capacidad integer,
    precio numeric(10, 2),
    destino integer,
    CONSTRAINT alojamiento_pkey PRIMARY KEY (id_alojamiento)
);

CREATE TABLE IF NOT EXISTS public.paquete
(
    id_paquete serial NOT NULL,
    nombre character varying(100) COLLATE pg_catalog."default",
    descripcion character varying(255) COLLATE pg_catalog."default",
    precio numeric(10, 0),
    cupos_totales integer,
    cupos_disponibles integer,
    fecha_inicio date,
    fecha_fin date,
    tipo character varying(50) COLLATE pg_catalog."default",
    disponible text COLLATE pg_catalog."default",
    vuelo integer,
    vehiculo integer,
    alojamiento integer,
    excursion integer,
    CONSTRAINT paquete_pkey PRIMARY KEY (id_paquete)
);

CREATE TABLE IF NOT EXISTS public.vehiculo_alquiler
(
    id_vehiculo serial NOT NULL,
    marca character varying(50) COLLATE pg_catalog."default",
    modelo character varying(50) COLLATE pg_catalog."default",
    capacidad integer,
    destino integer,
    CONSTRAINT vehiculo_alquiler_pkey PRIMARY KEY (id_vehiculo)
);

CREATE TABLE IF NOT EXISTS public.vuelo
(
    id_vuelo serial NOT NULL,
    aerolinea character varying(100) COLLATE pg_catalog."default",
    aeropuerto_o character varying(100) COLLATE pg_catalog."default",
    aeropuerto_d character varying(100) COLLATE pg_catalog."default",
    fecha date,
    duracion character varying(50) COLLATE pg_catalog."default",
    precio numeric(10, 2),
    destino integer,
    CONSTRAINT vuelo_pkey PRIMARY KEY (id_vuelo)
);

CREATE TABLE IF NOT EXISTS public.reserva
(
    id_reserva serial NOT NULL,
    id_paquete integer,
    fecha_reserva date,
    cantidad_personas integer,
    id_usuario integer NOT NULL,
    estado boolean,
    observaciones text COLLATE pg_catalog."default",
    CONSTRAINT reserva_pkey PRIMARY KEY (id_reserva)
);

CREATE TABLE IF NOT EXISTS public.usuario
(
    id_usuario serial NOT NULL,
    nombre character varying(250) COLLATE pg_catalog."default",
    apellido character varying(250) COLLATE pg_catalog."default",
    email character varying(250) COLLATE pg_catalog."default",
    "contraseña" character varying COLLATE pg_catalog."default",
    id_rol integer,
    CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario)
);

CREATE TABLE IF NOT EXISTS public.rol
(
    id_rol serial NOT NULL,
    tipo_rol character varying(50) COLLATE pg_catalog."default",
    permisos_rol character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT rol_pkey PRIMARY KEY (id_rol)
);

CREATE TABLE IF NOT EXISTS public.recuperacion_cuenta
(
    id_restablecer serial NOT NULL,
    codigo character varying(255) COLLATE pg_catalog."default",
    codigo_hash character varying(255) COLLATE pg_catalog."default",
    expiracion timestamp without time zone,
    usuario integer NOT NULL,
    CONSTRAINT recuperacion_cuenta_pkey PRIMARY KEY (id_restablecer)
);

CREATE TABLE IF NOT EXISTS public.reporte
(
    id_reporte serial NOT NULL,
    id_usuario integer NOT NULL,
    tipo_reporte character varying(50) COLLATE pg_catalog."default",
    fecha_generacion date,
    contenido text COLLATE pg_catalog."default",
    parametros text COLLATE pg_catalog."default",
    CONSTRAINT reporte_pkey PRIMARY KEY (id_reporte)
);

CREATE TABLE IF NOT EXISTS public.sesion_usuario
(
    id_sesion serial NOT NULL,
    fecha_sesion timestamp without time zone,
    ip_address character varying(250) COLLATE pg_catalog."default",
    sesion_activa boolean,
    id_usuario integer NOT NULL,
    CONSTRAINT sesion_usuario_pkey PRIMARY KEY (id_sesion)
);

CREATE TABLE IF NOT EXISTS public.carrito
(
    id_carrito serial NOT NULL,
    reserva integer NOT NULL,
    fecha_carrito date,
    precio_final numeric(10, 2),
    metodo_pago character varying(50) COLLATE pg_catalog."default",
    estado_pago character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT carrito_pkey PRIMARY KEY (id_carrito)
);

CREATE TABLE IF NOT EXISTS public.ventas
(
    id_venta serial NOT NULL,
    id_reserva integer NOT NULL,
    fecha_entrega date,
    monto_cobrado numeric(10, 2),
    CONSTRAINT ventas_pkey PRIMARY KEY (id_venta)
);

ALTER TABLE IF EXISTS public.excursion
    ADD CONSTRAINT fk_excursion_destino FOREIGN KEY (destino)
    REFERENCES public.destino (id_destino) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.alojamiento
    ADD CONSTRAINT fk_alojamiento_destino FOREIGN KEY (destino)
    REFERENCES public.destino (id_destino) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.paquete
    ADD CONSTRAINT fk_paquete_alojamiento FOREIGN KEY (alojamiento)
    REFERENCES public.alojamiento (id_alojamiento) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.paquete
    ADD CONSTRAINT fk_paquete_excursion FOREIGN KEY (excursion)
    REFERENCES public.excursion (id_excursion) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.paquete
    ADD CONSTRAINT fk_paquete_vehiculo FOREIGN KEY (vehiculo)
    REFERENCES public.vehiculo_alquiler (id_vehiculo) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.paquete
    ADD CONSTRAINT fk_paquete_vuelo FOREIGN KEY (vuelo)
    REFERENCES public.vuelo (id_vuelo) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.vehiculo_alquiler
    ADD CONSTRAINT fk_vehiculo_destino FOREIGN KEY (destino)
    REFERENCES public.destino (id_destino) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.vuelo
    ADD CONSTRAINT fk_vuelo_destino FOREIGN KEY (destino)
    REFERENCES public.destino (id_destino) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.reserva
    ADD CONSTRAINT fk_reserva_paquete FOREIGN KEY (id_paquete)
    REFERENCES public.paquete (id_paquete) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.reserva
    ADD CONSTRAINT fk_reserva_usuario FOREIGN KEY (id_usuario)
    REFERENCES public.usuario (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.usuario
    ADD CONSTRAINT fk_rol_id FOREIGN KEY (id_rol)
    REFERENCES public.rol (id_rol) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.recuperacion_cuenta
    ADD CONSTRAINT fk_recuperacion_usuario FOREIGN KEY (usuario)
    REFERENCES public.usuario (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.reporte
    ADD CONSTRAINT fk_reporte_usuario FOREIGN KEY (id_usuario)
    REFERENCES public.usuario (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.sesion_usuario
    ADD CONSTRAINT fk_sesion_usuario FOREIGN KEY (id_usuario)
    REFERENCES public.usuario (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.carrito
    ADD CONSTRAINT fk_carrito_reserva FOREIGN KEY (reserva)
    REFERENCES public.reserva (id_reserva) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.ventas
    ADD CONSTRAINT fk_ventas_reserva FOREIGN KEY (id_reserva)
    REFERENCES public.reserva (id_reserva) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;