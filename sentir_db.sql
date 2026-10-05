--
-- PostgreSQL database dump
--

\restrict QMEEE3CenaJGXUuGWJaMpHyk362SNDSsDkmldatbuT7ijaob8u62mfnYd5JZvEn

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

-- Started on 2026-10-05 16:39:15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 222 (class 1259 OID 16492)
-- Name: emergencias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.emergencias (
    id_emergencia integer NOT NULL,
    tipo character varying(50) NOT NULL,
    descripcion character varying(255) NOT NULL,
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    estado character varying(30) DEFAULT 'REPORTADA'::character varying,
    id_persona integer NOT NULL
);


ALTER TABLE public.emergencias OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16491)
-- Name: emergencias_id_emergencia_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.emergencias_id_emergencia_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.emergencias_id_emergencia_seq OWNER TO postgres;

--
-- TOC entry 4936 (class 0 OID 0)
-- Dependencies: 221
-- Name: emergencias_id_emergencia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.emergencias_id_emergencia_seq OWNED BY public.emergencias.id_emergencia;


--
-- TOC entry 220 (class 1259 OID 16390)
-- Name: personas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.personas (
    id_persona integer NOT NULL,
    nombre character varying(50) NOT NULL,
    telefono character varying(20) NOT NULL,
    tipo_persona character varying(15) NOT NULL
);


ALTER TABLE public.personas OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16389)
-- Name: personas_id_persona_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.personas_id_persona_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.personas_id_persona_seq OWNER TO postgres;

--
-- TOC entry 4937 (class 0 OID 0)
-- Dependencies: 219
-- Name: personas_id_persona_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.personas_id_persona_seq OWNED BY public.personas.id_persona;


--
-- TOC entry 224 (class 1259 OID 16510)
-- Name: ubicaciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ubicaciones (
    id_ubicacion integer NOT NULL,
    latitud numeric(10,7) NOT NULL,
    longitud numeric(10,7) NOT NULL,
    direccion character varying(255),
    id_emergencia integer NOT NULL
);


ALTER TABLE public.ubicaciones OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16509)
-- Name: ubicaciones_id_ubicacion_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ubicaciones_id_ubicacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ubicaciones_id_ubicacion_seq OWNER TO postgres;

--
-- TOC entry 4938 (class 0 OID 0)
-- Dependencies: 223
-- Name: ubicaciones_id_ubicacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ubicaciones_id_ubicacion_seq OWNED BY public.ubicaciones.id_ubicacion;


--
-- TOC entry 4766 (class 2604 OID 16495)
-- Name: emergencias id_emergencia; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emergencias ALTER COLUMN id_emergencia SET DEFAULT nextval('public.emergencias_id_emergencia_seq'::regclass);


--
-- TOC entry 4765 (class 2604 OID 16393)
-- Name: personas id_persona; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personas ALTER COLUMN id_persona SET DEFAULT nextval('public.personas_id_persona_seq'::regclass);


--
-- TOC entry 4769 (class 2604 OID 16513)
-- Name: ubicaciones id_ubicacion; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones ALTER COLUMN id_ubicacion SET DEFAULT nextval('public.ubicaciones_id_ubicacion_seq'::regclass);


--
-- TOC entry 4928 (class 0 OID 16492)
-- Dependencies: 222
-- Data for Name: emergencias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.emergencias (id_emergencia, tipo, descripcion, fecha, estado, id_persona) FROM stdin;
1	ACCIDENTE	Accidente cerca de la universidad	2026-10-05 16:11:56.220175	REPORTADA	1
\.


--
-- TOC entry 4926 (class 0 OID 16390)
-- Dependencies: 220
-- Data for Name: personas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.personas (id_persona, nombre, telefono, tipo_persona) FROM stdin;
1	Didier Guerrero Sumalave	3208777146	Docente
3	Adrian Trigos	3203525449	Estudiante
5	Laura Gómez	3001234567	CIUDADANO
\.


--
-- TOC entry 4930 (class 0 OID 16510)
-- Dependencies: 224
-- Data for Name: ubicaciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ubicaciones (id_ubicacion, latitud, longitud, direccion, id_emergencia) FROM stdin;
1	8.2501234	-73.3556789	Calle 10 # 5-20	1
\.


--
-- TOC entry 4939 (class 0 OID 0)
-- Dependencies: 221
-- Name: emergencias_id_emergencia_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.emergencias_id_emergencia_seq', 4, true);


--
-- TOC entry 4940 (class 0 OID 0)
-- Dependencies: 219
-- Name: personas_id_persona_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.personas_id_persona_seq', 5, true);


--
-- TOC entry 4941 (class 0 OID 0)
-- Dependencies: 223
-- Name: ubicaciones_id_ubicacion_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ubicaciones_id_ubicacion_seq', 1, true);


--
-- TOC entry 4773 (class 2606 OID 16503)
-- Name: emergencias emergencias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emergencias
    ADD CONSTRAINT emergencias_pkey PRIMARY KEY (id_emergencia);


--
-- TOC entry 4771 (class 2606 OID 16399)
-- Name: personas personas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_pkey PRIMARY KEY (id_persona);


--
-- TOC entry 4775 (class 2606 OID 16519)
-- Name: ubicaciones ubicaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones
    ADD CONSTRAINT ubicaciones_pkey PRIMARY KEY (id_ubicacion);


--
-- TOC entry 4776 (class 2606 OID 16504)
-- Name: emergencias fk_emergencia_persona; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emergencias
    ADD CONSTRAINT fk_emergencia_persona FOREIGN KEY (id_persona) REFERENCES public.personas(id_persona);


--
-- TOC entry 4777 (class 2606 OID 16520)
-- Name: ubicaciones fk_ubicacion_emergencia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ubicaciones
    ADD CONSTRAINT fk_ubicacion_emergencia FOREIGN KEY (id_emergencia) REFERENCES public.emergencias(id_emergencia);


-- Completed on 2026-10-05 16:39:15

--
-- PostgreSQL database dump complete
--

\unrestrict QMEEE3CenaJGXUuGWJaMpHyk362SNDSsDkmldatbuT7ijaob8u62mfnYd5JZvEn

