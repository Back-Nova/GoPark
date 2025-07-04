PGDMP                      }         	   GoPark_V2    17.4    17.4 v    K           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            L           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            M           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            N           1262    17608 	   GoPark_V2    DATABASE     q   CREATE DATABASE "GoPark_V2" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'es-AR';
    DROP DATABASE "GoPark_V2";
                     postgres    false            �            1259    17638    alojamiento    TABLE       CREATE TABLE public.alojamiento (
    id_alojamiento integer NOT NULL,
    nombre character varying(100),
    descripcion character varying(255),
    tipo_alojamiento character varying(50),
    capacidad integer,
    precio numeric(10,2),
    destino integer
);
    DROP TABLE public.alojamiento;
       public         heap r       postgres    false            �            1259    17637    alojamiento_id_alojamiento_seq    SEQUENCE     �   CREATE SEQUENCE public.alojamiento_id_alojamiento_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.alojamiento_id_alojamiento_seq;
       public               postgres    false    224            O           0    0    alojamiento_id_alojamiento_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.alojamiento_id_alojamiento_seq OWNED BY public.alojamiento.id_alojamiento;
          public               postgres    false    223            �            1259    17734    carrito    TABLE     �   CREATE TABLE public.carrito (
    id_carrito integer NOT NULL,
    reserva integer NOT NULL,
    fecha_carrito date,
    precio_final numeric(10,2),
    metodo_pago character varying(50),
    estado_pago character varying(50)
);
    DROP TABLE public.carrito;
       public         heap r       postgres    false            �            1259    17733    carrito_id_carrito_seq    SEQUENCE     �   CREATE SEQUENCE public.carrito_id_carrito_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.carrito_id_carrito_seq;
       public               postgres    false    236            P           0    0    carrito_id_carrito_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.carrito_id_carrito_seq OWNED BY public.carrito.id_carrito;
          public               postgres    false    235            �            1259    17629    destino    TABLE     �   CREATE TABLE public.destino (
    id_destino integer NOT NULL,
    pais character varying(50),
    ciudad character varying(100),
    region character varying(100),
    descripcion text
);
    DROP TABLE public.destino;
       public         heap r       postgres    false            �            1259    17628    destino_id_destino_seq    SEQUENCE     �   CREATE SEQUENCE public.destino_id_destino_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.destino_id_destino_seq;
       public               postgres    false    222            Q           0    0    destino_id_destino_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.destino_id_destino_seq OWNED BY public.destino.id_destino;
          public               postgres    false    221            �            1259    17674 	   excursion    TABLE     3  CREATE TABLE public.excursion (
    id_excursion integer NOT NULL,
    nombre character varying(100),
    descripcion character varying(255),
    duracion character varying(50),
    precio_adulto numeric(10,2),
    precio_nino numeric(10,2),
    participantes character varying(100),
    destino integer
);
    DROP TABLE public.excursion;
       public         heap r       postgres    false            �            1259    17673    excursion_id_excursion_seq    SEQUENCE     �   CREATE SEQUENCE public.excursion_id_excursion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.excursion_id_excursion_seq;
       public               postgres    false    230            R           0    0    excursion_id_excursion_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.excursion_id_excursion_seq OWNED BY public.excursion.id_excursion;
          public               postgres    false    229            �            1259    17688    paquete    TABLE     �  CREATE TABLE public.paquete (
    id_paquete integer NOT NULL,
    nombre character varying(100),
    descripcion character varying(255),
    precio numeric(10,0),
    cupos_totales integer,
    cupos_disponibles integer,
    fecha_inicio date,
    fecha_fin date,
    tipo character varying(50),
    disponible text,
    vuelo integer,
    vehiculo integer,
    alojamiento integer,
    excursion integer
);
    DROP TABLE public.paquete;
       public         heap r       postgres    false            �            1259    17687    paquete_id_paquete_seq    SEQUENCE     �   CREATE SEQUENCE public.paquete_id_paquete_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.paquete_id_paquete_seq;
       public               postgres    false    232            S           0    0    paquete_id_paquete_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.paquete_id_paquete_seq OWNED BY public.paquete.id_paquete;
          public               postgres    false    231            �            1259    17758    recuperacion_cuenta    TABLE     �   CREATE TABLE public.recuperacion_cuenta (
    id_restablecer integer NOT NULL,
    codigo character varying(255),
    codigo_hash character varying(255),
    expiracion timestamp without time zone,
    usuario integer NOT NULL
);
 '   DROP TABLE public.recuperacion_cuenta;
       public         heap r       postgres    false            �            1259    17757 &   recuperacion_cuenta_id_restablecer_seq    SEQUENCE     �   CREATE SEQUENCE public.recuperacion_cuenta_id_restablecer_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 =   DROP SEQUENCE public.recuperacion_cuenta_id_restablecer_seq;
       public               postgres    false    240            T           0    0 &   recuperacion_cuenta_id_restablecer_seq    SEQUENCE OWNED BY     q   ALTER SEQUENCE public.recuperacion_cuenta_id_restablecer_seq OWNED BY public.recuperacion_cuenta.id_restablecer;
          public               postgres    false    239            �            1259    17772    reporte    TABLE     �   CREATE TABLE public.reporte (
    id_reporte integer NOT NULL,
    id_usuario integer NOT NULL,
    tipo_reporte character varying(50),
    fecha_generacion date,
    contenido text,
    parametros text
);
    DROP TABLE public.reporte;
       public         heap r       postgres    false            �            1259    17771    reporte_id_reporte_seq    SEQUENCE     �   CREATE SEQUENCE public.reporte_id_reporte_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.reporte_id_reporte_seq;
       public               postgres    false    242            U           0    0    reporte_id_reporte_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.reporte_id_reporte_seq OWNED BY public.reporte.id_reporte;
          public               postgres    false    241            �            1259    17715    reserva    TABLE     �   CREATE TABLE public.reserva (
    id_reserva integer NOT NULL,
    id_paquete integer,
    fecha_reserva date,
    cantidad_personas integer,
    id_usuario integer NOT NULL,
    estado boolean,
    observaciones text
);
    DROP TABLE public.reserva;
       public         heap r       postgres    false            �            1259    17714    reserva_id_reserva_seq    SEQUENCE     �   CREATE SEQUENCE public.reserva_id_reserva_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.reserva_id_reserva_seq;
       public               postgres    false    234            V           0    0    reserva_id_reserva_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.reserva_id_reserva_seq OWNED BY public.reserva.id_reserva;
          public               postgres    false    233            �            1259    17610    rol    TABLE     �   CREATE TABLE public.rol (
    id_rol integer NOT NULL,
    tipo_rol character varying(50),
    permisos_rol character varying(255)
);
    DROP TABLE public.rol;
       public         heap r       postgres    false            �            1259    17609    rol_id_rol_seq    SEQUENCE     �   CREATE SEQUENCE public.rol_id_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.rol_id_rol_seq;
       public               postgres    false    218            W           0    0    rol_id_rol_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.rol_id_rol_seq OWNED BY public.rol.id_rol;
          public               postgres    false    217            �            1259    17786    sesion_usuario    TABLE     �   CREATE TABLE public.sesion_usuario (
    id_sesion integer NOT NULL,
    fecha_sesion timestamp without time zone,
    ip_address character varying(250),
    sesion_activa boolean,
    id_usuario integer NOT NULL
);
 "   DROP TABLE public.sesion_usuario;
       public         heap r       postgres    false            �            1259    17785    sesion_usuario_id_sesion_seq    SEQUENCE     �   CREATE SEQUENCE public.sesion_usuario_id_sesion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.sesion_usuario_id_sesion_seq;
       public               postgres    false    244            X           0    0    sesion_usuario_id_sesion_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.sesion_usuario_id_sesion_seq OWNED BY public.sesion_usuario.id_sesion;
          public               postgres    false    243            �            1259    17617    usuario    TABLE     �   CREATE TABLE public.usuario (
    id_usuario integer NOT NULL,
    nombre character varying(250),
    apellido character varying(250),
    email character varying(250),
    "contraseña" character varying,
    id_rol integer
);
    DROP TABLE public.usuario;
       public         heap r       postgres    false            �            1259    17616    usuario_id_usuario_seq    SEQUENCE     �   CREATE SEQUENCE public.usuario_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.usuario_id_usuario_seq;
       public               postgres    false    220            Y           0    0    usuario_id_usuario_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.usuario_id_usuario_seq OWNED BY public.usuario.id_usuario;
          public               postgres    false    219            �            1259    17650    vehiculo_alquiler    TABLE     �   CREATE TABLE public.vehiculo_alquiler (
    id_vehiculo integer NOT NULL,
    marca character varying(50),
    modelo character varying(50),
    capacidad integer,
    destino integer
);
 %   DROP TABLE public.vehiculo_alquiler;
       public         heap r       postgres    false            �            1259    17649 !   vehiculo_alquiler_id_vehiculo_seq    SEQUENCE     �   CREATE SEQUENCE public.vehiculo_alquiler_id_vehiculo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.vehiculo_alquiler_id_vehiculo_seq;
       public               postgres    false    226            Z           0    0 !   vehiculo_alquiler_id_vehiculo_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.vehiculo_alquiler_id_vehiculo_seq OWNED BY public.vehiculo_alquiler.id_vehiculo;
          public               postgres    false    225            �            1259    17746    ventas    TABLE     �   CREATE TABLE public.ventas (
    id_venta integer NOT NULL,
    id_reserva integer NOT NULL,
    fecha_entrega date,
    monto_cobrado numeric(10,2)
);
    DROP TABLE public.ventas;
       public         heap r       postgres    false            �            1259    17745    ventas_id_venta_seq    SEQUENCE     �   CREATE SEQUENCE public.ventas_id_venta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.ventas_id_venta_seq;
       public               postgres    false    238            [           0    0    ventas_id_venta_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.ventas_id_venta_seq OWNED BY public.ventas.id_venta;
          public               postgres    false    237            �            1259    17662    vuelo    TABLE       CREATE TABLE public.vuelo (
    id_vuelo integer NOT NULL,
    aerolinea character varying(100),
    aeropuerto_o character varying(100),
    aeropuerto_d character varying(100),
    fecha date,
    duracion character varying(50),
    precio numeric(10,2),
    destino integer
);
    DROP TABLE public.vuelo;
       public         heap r       postgres    false            �            1259    17661    vuelo_id_vuelo_seq    SEQUENCE     �   CREATE SEQUENCE public.vuelo_id_vuelo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.vuelo_id_vuelo_seq;
       public               postgres    false    228            \           0    0    vuelo_id_vuelo_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.vuelo_id_vuelo_seq OWNED BY public.vuelo.id_vuelo;
          public               postgres    false    227            e           2604    17641    alojamiento id_alojamiento    DEFAULT     �   ALTER TABLE ONLY public.alojamiento ALTER COLUMN id_alojamiento SET DEFAULT nextval('public.alojamiento_id_alojamiento_seq'::regclass);
 I   ALTER TABLE public.alojamiento ALTER COLUMN id_alojamiento DROP DEFAULT;
       public               postgres    false    223    224    224            k           2604    17737    carrito id_carrito    DEFAULT     x   ALTER TABLE ONLY public.carrito ALTER COLUMN id_carrito SET DEFAULT nextval('public.carrito_id_carrito_seq'::regclass);
 A   ALTER TABLE public.carrito ALTER COLUMN id_carrito DROP DEFAULT;
       public               postgres    false    235    236    236            d           2604    17632    destino id_destino    DEFAULT     x   ALTER TABLE ONLY public.destino ALTER COLUMN id_destino SET DEFAULT nextval('public.destino_id_destino_seq'::regclass);
 A   ALTER TABLE public.destino ALTER COLUMN id_destino DROP DEFAULT;
       public               postgres    false    222    221    222            h           2604    17677    excursion id_excursion    DEFAULT     �   ALTER TABLE ONLY public.excursion ALTER COLUMN id_excursion SET DEFAULT nextval('public.excursion_id_excursion_seq'::regclass);
 E   ALTER TABLE public.excursion ALTER COLUMN id_excursion DROP DEFAULT;
       public               postgres    false    230    229    230            i           2604    17691    paquete id_paquete    DEFAULT     x   ALTER TABLE ONLY public.paquete ALTER COLUMN id_paquete SET DEFAULT nextval('public.paquete_id_paquete_seq'::regclass);
 A   ALTER TABLE public.paquete ALTER COLUMN id_paquete DROP DEFAULT;
       public               postgres    false    231    232    232            m           2604    17761 "   recuperacion_cuenta id_restablecer    DEFAULT     �   ALTER TABLE ONLY public.recuperacion_cuenta ALTER COLUMN id_restablecer SET DEFAULT nextval('public.recuperacion_cuenta_id_restablecer_seq'::regclass);
 Q   ALTER TABLE public.recuperacion_cuenta ALTER COLUMN id_restablecer DROP DEFAULT;
       public               postgres    false    239    240    240            n           2604    17775    reporte id_reporte    DEFAULT     x   ALTER TABLE ONLY public.reporte ALTER COLUMN id_reporte SET DEFAULT nextval('public.reporte_id_reporte_seq'::regclass);
 A   ALTER TABLE public.reporte ALTER COLUMN id_reporte DROP DEFAULT;
       public               postgres    false    241    242    242            j           2604    17718    reserva id_reserva    DEFAULT     x   ALTER TABLE ONLY public.reserva ALTER COLUMN id_reserva SET DEFAULT nextval('public.reserva_id_reserva_seq'::regclass);
 A   ALTER TABLE public.reserva ALTER COLUMN id_reserva DROP DEFAULT;
       public               postgres    false    234    233    234            b           2604    17613 
   rol id_rol    DEFAULT     h   ALTER TABLE ONLY public.rol ALTER COLUMN id_rol SET DEFAULT nextval('public.rol_id_rol_seq'::regclass);
 9   ALTER TABLE public.rol ALTER COLUMN id_rol DROP DEFAULT;
       public               postgres    false    218    217    218            o           2604    17789    sesion_usuario id_sesion    DEFAULT     �   ALTER TABLE ONLY public.sesion_usuario ALTER COLUMN id_sesion SET DEFAULT nextval('public.sesion_usuario_id_sesion_seq'::regclass);
 G   ALTER TABLE public.sesion_usuario ALTER COLUMN id_sesion DROP DEFAULT;
       public               postgres    false    244    243    244            c           2604    17620    usuario id_usuario    DEFAULT     x   ALTER TABLE ONLY public.usuario ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuario_id_usuario_seq'::regclass);
 A   ALTER TABLE public.usuario ALTER COLUMN id_usuario DROP DEFAULT;
       public               postgres    false    220    219    220            f           2604    17653    vehiculo_alquiler id_vehiculo    DEFAULT     �   ALTER TABLE ONLY public.vehiculo_alquiler ALTER COLUMN id_vehiculo SET DEFAULT nextval('public.vehiculo_alquiler_id_vehiculo_seq'::regclass);
 L   ALTER TABLE public.vehiculo_alquiler ALTER COLUMN id_vehiculo DROP DEFAULT;
       public               postgres    false    226    225    226            l           2604    17749    ventas id_venta    DEFAULT     r   ALTER TABLE ONLY public.ventas ALTER COLUMN id_venta SET DEFAULT nextval('public.ventas_id_venta_seq'::regclass);
 >   ALTER TABLE public.ventas ALTER COLUMN id_venta DROP DEFAULT;
       public               postgres    false    238    237    238            g           2604    17665    vuelo id_vuelo    DEFAULT     p   ALTER TABLE ONLY public.vuelo ALTER COLUMN id_vuelo SET DEFAULT nextval('public.vuelo_id_vuelo_seq'::regclass);
 =   ALTER TABLE public.vuelo ALTER COLUMN id_vuelo DROP DEFAULT;
       public               postgres    false    227    228    228            4          0    17638    alojamiento 
   TABLE DATA           x   COPY public.alojamiento (id_alojamiento, nombre, descripcion, tipo_alojamiento, capacidad, precio, destino) FROM stdin;
    public               postgres    false    224   �       @          0    17734    carrito 
   TABLE DATA           m   COPY public.carrito (id_carrito, reserva, fecha_carrito, precio_final, metodo_pago, estado_pago) FROM stdin;
    public               postgres    false    236   Q�       2          0    17629    destino 
   TABLE DATA           P   COPY public.destino (id_destino, pais, ciudad, region, descripcion) FROM stdin;
    public               postgres    false    222   n�       :          0    17674 	   excursion 
   TABLE DATA           �   COPY public.excursion (id_excursion, nombre, descripcion, duracion, precio_adulto, precio_nino, participantes, destino) FROM stdin;
    public               postgres    false    230   ��       <          0    17688    paquete 
   TABLE DATA           �   COPY public.paquete (id_paquete, nombre, descripcion, precio, cupos_totales, cupos_disponibles, fecha_inicio, fecha_fin, tipo, disponible, vuelo, vehiculo, alojamiento, excursion) FROM stdin;
    public               postgres    false    232   b�       D          0    17758    recuperacion_cuenta 
   TABLE DATA           g   COPY public.recuperacion_cuenta (id_restablecer, codigo, codigo_hash, expiracion, usuario) FROM stdin;
    public               postgres    false    240   ϔ       F          0    17772    reporte 
   TABLE DATA           p   COPY public.reporte (id_reporte, id_usuario, tipo_reporte, fecha_generacion, contenido, parametros) FROM stdin;
    public               postgres    false    242   ��       >          0    17715    reserva 
   TABLE DATA           ~   COPY public.reserva (id_reserva, id_paquete, fecha_reserva, cantidad_personas, id_usuario, estado, observaciones) FROM stdin;
    public               postgres    false    234   Ɩ       .          0    17610    rol 
   TABLE DATA           =   COPY public.rol (id_rol, tipo_rol, permisos_rol) FROM stdin;
    public               postgres    false    218   �       H          0    17786    sesion_usuario 
   TABLE DATA           h   COPY public.sesion_usuario (id_sesion, fecha_sesion, ip_address, sesion_activa, id_usuario) FROM stdin;
    public               postgres    false    244   )�       0          0    17617    usuario 
   TABLE DATA           ]   COPY public.usuario (id_usuario, nombre, apellido, email, "contraseña", id_rol) FROM stdin;
    public               postgres    false    220   ��       6          0    17650    vehiculo_alquiler 
   TABLE DATA           [   COPY public.vehiculo_alquiler (id_vehiculo, marca, modelo, capacidad, destino) FROM stdin;
    public               postgres    false    226   ��       B          0    17746    ventas 
   TABLE DATA           T   COPY public.ventas (id_venta, id_reserva, fecha_entrega, monto_cobrado) FROM stdin;
    public               postgres    false    238   י       8          0    17662    vuelo 
   TABLE DATA           r   COPY public.vuelo (id_vuelo, aerolinea, aeropuerto_o, aeropuerto_d, fecha, duracion, precio, destino) FROM stdin;
    public               postgres    false    228   ��       ]           0    0    alojamiento_id_alojamiento_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.alojamiento_id_alojamiento_seq', 57, true);
          public               postgres    false    223            ^           0    0    carrito_id_carrito_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.carrito_id_carrito_seq', 1, false);
          public               postgres    false    235            _           0    0    destino_id_destino_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.destino_id_destino_seq', 10, true);
          public               postgres    false    221            `           0    0    excursion_id_excursion_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.excursion_id_excursion_seq', 49, true);
          public               postgres    false    229            a           0    0    paquete_id_paquete_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.paquete_id_paquete_seq', 7, true);
          public               postgres    false    231            b           0    0 &   recuperacion_cuenta_id_restablecer_seq    SEQUENCE SET     T   SELECT pg_catalog.setval('public.recuperacion_cuenta_id_restablecer_seq', 7, true);
          public               postgres    false    239            c           0    0    reporte_id_reporte_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.reporte_id_reporte_seq', 1, false);
          public               postgres    false    241            d           0    0    reserva_id_reserva_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.reserva_id_reserva_seq', 1, false);
          public               postgres    false    233            e           0    0    rol_id_rol_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.rol_id_rol_seq', 5, true);
          public               postgres    false    217            f           0    0    sesion_usuario_id_sesion_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.sesion_usuario_id_sesion_seq', 6, true);
          public               postgres    false    243            g           0    0    usuario_id_usuario_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.usuario_id_usuario_seq', 10, true);
          public               postgres    false    219            h           0    0 !   vehiculo_alquiler_id_vehiculo_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.vehiculo_alquiler_id_vehiculo_seq', 28, true);
          public               postgres    false    225            i           0    0    ventas_id_venta_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.ventas_id_venta_seq', 1, false);
          public               postgres    false    237            j           0    0    vuelo_id_vuelo_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.vuelo_id_vuelo_seq', 21, true);
          public               postgres    false    227            w           2606    17643    alojamiento alojamiento_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.alojamiento
    ADD CONSTRAINT alojamiento_pkey PRIMARY KEY (id_alojamiento);
 F   ALTER TABLE ONLY public.alojamiento DROP CONSTRAINT alojamiento_pkey;
       public                 postgres    false    224            �           2606    17739    carrito carrito_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.carrito
    ADD CONSTRAINT carrito_pkey PRIMARY KEY (id_carrito);
 >   ALTER TABLE ONLY public.carrito DROP CONSTRAINT carrito_pkey;
       public                 postgres    false    236            u           2606    17636    destino destino_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.destino
    ADD CONSTRAINT destino_pkey PRIMARY KEY (id_destino);
 >   ALTER TABLE ONLY public.destino DROP CONSTRAINT destino_pkey;
       public                 postgres    false    222            }           2606    17681    excursion excursion_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.excursion
    ADD CONSTRAINT excursion_pkey PRIMARY KEY (id_excursion);
 B   ALTER TABLE ONLY public.excursion DROP CONSTRAINT excursion_pkey;
       public                 postgres    false    230                       2606    17693    paquete paquete_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.paquete
    ADD CONSTRAINT paquete_pkey PRIMARY KEY (id_paquete);
 >   ALTER TABLE ONLY public.paquete DROP CONSTRAINT paquete_pkey;
       public                 postgres    false    232            �           2606    17765 ,   recuperacion_cuenta recuperacion_cuenta_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY public.recuperacion_cuenta
    ADD CONSTRAINT recuperacion_cuenta_pkey PRIMARY KEY (id_restablecer);
 V   ALTER TABLE ONLY public.recuperacion_cuenta DROP CONSTRAINT recuperacion_cuenta_pkey;
       public                 postgres    false    240            �           2606    17779    reporte reporte_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT reporte_pkey PRIMARY KEY (id_reporte);
 >   ALTER TABLE ONLY public.reporte DROP CONSTRAINT reporte_pkey;
       public                 postgres    false    242            �           2606    17722    reserva reserva_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT reserva_pkey PRIMARY KEY (id_reserva);
 >   ALTER TABLE ONLY public.reserva DROP CONSTRAINT reserva_pkey;
       public                 postgres    false    234            q           2606    17615    rol rol_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pkey PRIMARY KEY (id_rol);
 6   ALTER TABLE ONLY public.rol DROP CONSTRAINT rol_pkey;
       public                 postgres    false    218            �           2606    17791 "   sesion_usuario sesion_usuario_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public.sesion_usuario
    ADD CONSTRAINT sesion_usuario_pkey PRIMARY KEY (id_sesion);
 L   ALTER TABLE ONLY public.sesion_usuario DROP CONSTRAINT sesion_usuario_pkey;
       public                 postgres    false    244            s           2606    17622    usuario usuario_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario);
 >   ALTER TABLE ONLY public.usuario DROP CONSTRAINT usuario_pkey;
       public                 postgres    false    220            y           2606    17655 (   vehiculo_alquiler vehiculo_alquiler_pkey 
   CONSTRAINT     o   ALTER TABLE ONLY public.vehiculo_alquiler
    ADD CONSTRAINT vehiculo_alquiler_pkey PRIMARY KEY (id_vehiculo);
 R   ALTER TABLE ONLY public.vehiculo_alquiler DROP CONSTRAINT vehiculo_alquiler_pkey;
       public                 postgres    false    226            �           2606    17751    ventas ventas_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_pkey PRIMARY KEY (id_venta);
 <   ALTER TABLE ONLY public.ventas DROP CONSTRAINT ventas_pkey;
       public                 postgres    false    238            {           2606    17667    vuelo vuelo_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.vuelo
    ADD CONSTRAINT vuelo_pkey PRIMARY KEY (id_vuelo);
 :   ALTER TABLE ONLY public.vuelo DROP CONSTRAINT vuelo_pkey;
       public                 postgres    false    228            �           2606    17644 "   alojamiento fk_alojamiento_destino    FK CONSTRAINT     �   ALTER TABLE ONLY public.alojamiento
    ADD CONSTRAINT fk_alojamiento_destino FOREIGN KEY (destino) REFERENCES public.destino(id_destino);
 L   ALTER TABLE ONLY public.alojamiento DROP CONSTRAINT fk_alojamiento_destino;
       public               postgres    false    4725    224    222            �           2606    17740    carrito fk_carrito_reserva    FK CONSTRAINT     �   ALTER TABLE ONLY public.carrito
    ADD CONSTRAINT fk_carrito_reserva FOREIGN KEY (reserva) REFERENCES public.reserva(id_reserva);
 D   ALTER TABLE ONLY public.carrito DROP CONSTRAINT fk_carrito_reserva;
       public               postgres    false    234    4737    236            �           2606    17682    excursion fk_excursion_destino    FK CONSTRAINT     �   ALTER TABLE ONLY public.excursion
    ADD CONSTRAINT fk_excursion_destino FOREIGN KEY (destino) REFERENCES public.destino(id_destino);
 H   ALTER TABLE ONLY public.excursion DROP CONSTRAINT fk_excursion_destino;
       public               postgres    false    4725    222    230            �           2606    17704    paquete fk_paquete_alojamiento    FK CONSTRAINT     �   ALTER TABLE ONLY public.paquete
    ADD CONSTRAINT fk_paquete_alojamiento FOREIGN KEY (alojamiento) REFERENCES public.alojamiento(id_alojamiento);
 H   ALTER TABLE ONLY public.paquete DROP CONSTRAINT fk_paquete_alojamiento;
       public               postgres    false    224    4727    232            �           2606    17709    paquete fk_paquete_excursion    FK CONSTRAINT     �   ALTER TABLE ONLY public.paquete
    ADD CONSTRAINT fk_paquete_excursion FOREIGN KEY (excursion) REFERENCES public.excursion(id_excursion);
 F   ALTER TABLE ONLY public.paquete DROP CONSTRAINT fk_paquete_excursion;
       public               postgres    false    232    4733    230            �           2606    17699    paquete fk_paquete_vehiculo    FK CONSTRAINT     �   ALTER TABLE ONLY public.paquete
    ADD CONSTRAINT fk_paquete_vehiculo FOREIGN KEY (vehiculo) REFERENCES public.vehiculo_alquiler(id_vehiculo);
 E   ALTER TABLE ONLY public.paquete DROP CONSTRAINT fk_paquete_vehiculo;
       public               postgres    false    4729    232    226            �           2606    17694    paquete fk_paquete_vuelo    FK CONSTRAINT     {   ALTER TABLE ONLY public.paquete
    ADD CONSTRAINT fk_paquete_vuelo FOREIGN KEY (vuelo) REFERENCES public.vuelo(id_vuelo);
 B   ALTER TABLE ONLY public.paquete DROP CONSTRAINT fk_paquete_vuelo;
       public               postgres    false    4731    228    232            �           2606    17766 +   recuperacion_cuenta fk_recuperacion_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.recuperacion_cuenta
    ADD CONSTRAINT fk_recuperacion_usuario FOREIGN KEY (usuario) REFERENCES public.usuario(id_usuario);
 U   ALTER TABLE ONLY public.recuperacion_cuenta DROP CONSTRAINT fk_recuperacion_usuario;
       public               postgres    false    240    220    4723            �           2606    17780    reporte fk_reporte_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.reporte
    ADD CONSTRAINT fk_reporte_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario);
 D   ALTER TABLE ONLY public.reporte DROP CONSTRAINT fk_reporte_usuario;
       public               postgres    false    4723    220    242            �           2606    17723    reserva fk_reserva_paquete    FK CONSTRAINT     �   ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT fk_reserva_paquete FOREIGN KEY (id_paquete) REFERENCES public.paquete(id_paquete);
 D   ALTER TABLE ONLY public.reserva DROP CONSTRAINT fk_reserva_paquete;
       public               postgres    false    234    4735    232            �           2606    17728    reserva fk_reserva_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.reserva
    ADD CONSTRAINT fk_reserva_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario);
 D   ALTER TABLE ONLY public.reserva DROP CONSTRAINT fk_reserva_usuario;
       public               postgres    false    234    4723    220            �           2606    17798    usuario fk_rol_id    FK CONSTRAINT     {   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT fk_rol_id FOREIGN KEY (id_rol) REFERENCES public.rol(id_rol) NOT VALID;
 ;   ALTER TABLE ONLY public.usuario DROP CONSTRAINT fk_rol_id;
       public               postgres    false    220    218    4721            �           2606    17792     sesion_usuario fk_sesion_usuario    FK CONSTRAINT     �   ALTER TABLE ONLY public.sesion_usuario
    ADD CONSTRAINT fk_sesion_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario);
 J   ALTER TABLE ONLY public.sesion_usuario DROP CONSTRAINT fk_sesion_usuario;
       public               postgres    false    220    4723    244            �           2606    17656 %   vehiculo_alquiler fk_vehiculo_destino    FK CONSTRAINT     �   ALTER TABLE ONLY public.vehiculo_alquiler
    ADD CONSTRAINT fk_vehiculo_destino FOREIGN KEY (destino) REFERENCES public.destino(id_destino);
 O   ALTER TABLE ONLY public.vehiculo_alquiler DROP CONSTRAINT fk_vehiculo_destino;
       public               postgres    false    4725    222    226            �           2606    17752    ventas fk_ventas_reserva    FK CONSTRAINT     �   ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT fk_ventas_reserva FOREIGN KEY (id_reserva) REFERENCES public.reserva(id_reserva);
 B   ALTER TABLE ONLY public.ventas DROP CONSTRAINT fk_ventas_reserva;
       public               postgres    false    4737    238    234            �           2606    17668    vuelo fk_vuelo_destino    FK CONSTRAINT        ALTER TABLE ONLY public.vuelo
    ADD CONSTRAINT fk_vuelo_destino FOREIGN KEY (destino) REFERENCES public.destino(id_destino);
 @   ALTER TABLE ONLY public.vuelo DROP CONSTRAINT fk_vuelo_destino;
       public               postgres    false    222    4725    228            4   @   x�35���/I�QHIU�IT�+MJ�t-.IU� ��+$����Cqs�XZ�YZr�p��qqq p\�      @      x������ � �      2   }   x�U�1
1E�S�	��N$6�v6C6.ј�$Sx{��͇��v����b��]&IM��"JsH���p�Z���ԧ�ի��s1υ�
�|��x�����vG{ػ�z��?�m@�nd0+      :   W   x�-�1@0 �99EN�Y��`��Q�і���u��&��z1�)�S�V+��H�C�^��|���s��ҖL24������00�"~M�9      <   ]   x�E�A
� F���)��1Z*��S�����>wm/`IYNi�\Xkc��~{���'"�Kp������Ƈ��KMp.�GL����G�e      D   �  x�]��j�1��9W��c~�̷Ӷ�R�`EDI2[�vQ�����γ	I�3O�`�|�����'��~N@4iv��F�������<]�̑��R`�`/h&U�SM�g�ϰ�����[)U$'���w�����Gx{�8D$��(��in��,ٵ��9G�a�O�@[����OaeW����0N~?_�_�E1/.S2�6AtV�5���{C�C�����2�z���#�κS�,�Q=�$=�:��o5��V�[�1L�� Z�V��"bTo�{�iT��P\cq9!)���	�:i��o��G
/&�K� �'O�i}�*��FV
��q���F%;%�.����kU9=]>��p���:�٫2���:���LRWb�Z��#|�ٗ	��1���$;��K.GRI_��?��9M���!U%B��=8
����T�akP�����d���r;%�� X�H���>û"      F      x������ � �      >      x������ � �      .   6   x�3�LL����,�O�/�2��JMKUHIUK�+I,�
�q:�dR��=... q�      H   Q   x�Uʹ�0 ���F���,#�+R�8����'ǔ�ڵ�H�D&0���B�Ek�^I�!�G�_���f��J���x">�?      0   �  x�}��j�1���<Ǭ�/ٖ���E;����ƒ�t�̅���O_��Fsd�w���|��������æ��.l���vxٟ.V�K�����W{�����u�MZ�Lf���Z-1z�H2�:Ssm�ꥧ.���)(%�,-L(i�6w�9I�jI�(.�+Yp-Ԃf��+(Ny���ܶg�M�gk��ض���ϻ�Ǹ�՗n���9�sm2WJ��9r�bÑ�V��<��JkZ���#	�H�"91IeiR���u��T�&T��f�� ����'r��B����v�����Чx�Ƿ ^��/��~\���~������Pb�-|�:���~Y�\�\��]��Ww��n4��<�K�к�h�C�ԥ���}l��l��D������+m��E<�v��m\�Es��&}~�uu���~�|�	�����s.���e�U[rec�(��j� �,���G�ک�4�F�PYK1Z/\��B^���r�("��{'4?/��?�0�      6   6   x�32�ɯ�/I�tN,�����L�4�4�2����OO��420��4���qqq ?r~      B      x������ � �      8   P   x�32�tL-����KMTp,JO�+��KT�N�)I�t*M��/Vp�,J-�4200�50�54�4�(�-�@�Ғӄ+F��� r��     