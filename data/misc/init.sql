--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

DROP DATABASE IF EXISTS event_housing_db;
CREATE DATABASE event_housing_db;

\c event_housing_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: attendee_rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.attendee_rooms (
    room_id smallint NOT NULL,
    attendee_id smallint NOT NULL
);


ALTER TABLE public.attendee_rooms OWNER TO postgres;

--
-- Name: attendee_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.attendee_types (
    id smallint NOT NULL,
    name character varying(128) NOT NULL,
    access_code character varying(128)
);


ALTER TABLE public.attendee_types OWNER TO postgres;

--
-- Name: attendee_types_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.attendee_types_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.attendee_types_id_seq OWNER TO postgres;

--
-- Name: attendee_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.attendee_types_id_seq OWNED BY public.attendee_types.id;


--
-- Name: hotels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hotels (
    id smallint NOT NULL,
    name character varying(128) NOT NULL,
    address character varying(128) NOT NULL,
    city character varying(128) NOT NULL,
    state_abr character varying(2) NOT NULL,
    zip_code integer NOT NULL
);


ALTER TABLE public.hotels OWNER TO postgres;

--
-- Name: hotels_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.hotels_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hotels_id_seq OWNER TO postgres;

--
-- Name: hotels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.hotels_id_seq OWNED BY public.hotels.id;


--
-- Name: reservations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reservations (
    ack_num integer NOT NULL,
    first_name character varying(128) NOT NULL,
    last_name character varying(128) NOT NULL,
    check_in_date date NOT NULL,
    check_out_date date NOT NULL,
    address character varying(128) NOT NULL,
    city character varying(128) NOT NULL,
    state_abr character varying(2) NOT NULL,
    zip_code integer NOT NULL,
    room_id smallint NOT NULL,
    attendee_id smallint NOT NULL,
    hotel_id smallint NOT NULL,
    price_per_night double precision,
    number_of_nights smallint,
    total_stay_price double precision,
    revervation_created timestamp without time zone
);


ALTER TABLE public.reservations OWNER TO postgres;

--
-- Name: reservations_ack_num_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reservations_ack_num_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reservations_ack_num_seq OWNER TO postgres;

--
-- Name: reservations_ack_num_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reservations_ack_num_seq OWNED BY public.reservations.ack_num;


--
-- Name: room_inventories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.room_inventories (
    room_id smallint NOT NULL,
    date date NOT NULL,
    inventory smallint NOT NULL,
    CONSTRAINT room_inventories_inventory_check CHECK ((inventory >= 0))
);


ALTER TABLE public.room_inventories OWNER TO postgres;

--
-- Name: room_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.room_types (
    id smallint NOT NULL,
    hotel_id smallint NOT NULL,
    name character varying(128) NOT NULL,
    max_guests smallint NOT NULL,
    price double precision NOT NULL
);


ALTER TABLE public.room_types OWNER TO postgres;

--
-- Name: room_types_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.room_types_id_seq
    AS smallint
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.room_types_id_seq OWNER TO postgres;

--
-- Name: room_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.room_types_id_seq OWNED BY public.room_types.id;


--
-- Name: attendee_types id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendee_types ALTER COLUMN id SET DEFAULT nextval('public.attendee_types_id_seq'::regclass);


--
-- Name: hotels id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hotels ALTER COLUMN id SET DEFAULT nextval('public.hotels_id_seq'::regclass);


--
-- Name: reservations ack_num; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservations ALTER COLUMN ack_num SET DEFAULT nextval('public.reservations_ack_num_seq'::regclass);


--
-- Name: room_types id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room_types ALTER COLUMN id SET DEFAULT nextval('public.room_types_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
445ed6421360
\.


--
-- Data for Name: attendee_rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.attendee_rooms (room_id, attendee_id) FROM stdin;
1	1
2	1
3	1
2	2
4	2
5	2
5	4
6	3
4	4
\.


--
-- Data for Name: attendee_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.attendee_types (id, name, access_code) FROM stdin;
1	attendee	event_name_attendee
2	exhibitor	event_name_exhibitor
3	staff	staff_code
4	company	company_code
\.


--
-- Data for Name: hotels; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hotels (id, name, address, city, state_abr, zip_code) FROM stdin;
1	Hilton Alpharetta	178 Highland St.	Alpharetta	GA	30004
2	Hampton Cartersville	1999 Milton Ave.	Cartersville	GA	30059
3	Residence Inn Atlanta	779 Peachtree St.	Atlanta	GA	30548
\.


--
-- Data for Name: reservations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reservations (ack_num, first_name, last_name, check_in_date, check_out_date, address, city, state_abr, zip_code, room_id, attendee_id, hotel_id, price_per_night, number_of_nights, total_stay_price, revervation_created) FROM stdin;
\.


--
-- Data for Name: room_inventories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.room_inventories (room_id, date, inventory) FROM stdin;
1	2022-03-01	15
1	2022-03-02	15
1	2022-03-03	15
1	2022-03-04	15
2	2022-03-01	20
2	2022-03-02	20
2	2022-03-03	20
2	2022-03-04	20
3	2022-03-01	10
3	2022-03-02	10
3	2022-03-03	10
3	2022-03-04	10
4	2022-03-01	1
4	2022-03-02	1
4	2022-03-03	1
4	2022-03-04	1
5	2022-03-01	25
5	2022-03-02	25
5	2022-03-03	25
5	2022-03-04	25
\.


--
-- Data for Name: room_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.room_types (id, hotel_id, name, max_guests, price) FROM stdin;
1	1	Deluxe King	2	159.99
2	1	Deluxe Queen/Queen	4	175.99
3	2	King	2	139.99
4	2	Two Queens	4	149.99
5	2	Presidential Suite	8	259.99
6	3	One Bedroom Suite	4	209
\.


--
-- Name: attendee_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.attendee_types_id_seq', 4, true);


--
-- Name: hotels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hotels_id_seq', 3, true);


--
-- Name: reservations_ack_num_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reservations_ack_num_seq', 1, false);


--
-- Name: room_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.room_types_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: attendee_rooms attendee_rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendee_rooms
    ADD CONSTRAINT attendee_rooms_pkey PRIMARY KEY (room_id, attendee_id);


--
-- Name: attendee_types attendee_types_access_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendee_types
    ADD CONSTRAINT attendee_types_access_code_key UNIQUE (access_code);


--
-- Name: attendee_types attendee_types_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendee_types
    ADD CONSTRAINT attendee_types_name_key UNIQUE (name);


--
-- Name: attendee_types attendee_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendee_types
    ADD CONSTRAINT attendee_types_pkey PRIMARY KEY (id);


--
-- Name: hotels hotels_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hotels
    ADD CONSTRAINT hotels_name_key UNIQUE (name);


--
-- Name: hotels hotels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hotels
    ADD CONSTRAINT hotels_pkey PRIMARY KEY (id);


--
-- Name: reservations reservations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_pkey PRIMARY KEY (ack_num);


--
-- Name: room_inventories room_inventories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room_inventories
    ADD CONSTRAINT room_inventories_pkey PRIMARY KEY (room_id, date);


--
-- Name: room_types room_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room_types
    ADD CONSTRAINT room_types_pkey PRIMARY KEY (id);


--
-- Name: attendee_rooms attendee_rooms_attendee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendee_rooms
    ADD CONSTRAINT attendee_rooms_attendee_id_fkey FOREIGN KEY (attendee_id) REFERENCES public.attendee_types(id);


--
-- Name: attendee_rooms attendee_rooms_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attendee_rooms
    ADD CONSTRAINT attendee_rooms_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room_types(id);


--
-- Name: reservations reservations_attendee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_attendee_id_fkey FOREIGN KEY (attendee_id) REFERENCES public.attendee_types(id);


--
-- Name: reservations reservations_hotel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_hotel_id_fkey FOREIGN KEY (hotel_id) REFERENCES public.hotels(id);


--
-- Name: reservations reservations_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room_types(id);


--
-- Name: room_inventories room_inventories_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room_inventories
    ADD CONSTRAINT room_inventories_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room_types(id) ON DELETE CASCADE;


--
-- Name: room_types room_types_hotel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.room_types
    ADD CONSTRAINT room_types_hotel_id_fkey FOREIGN KEY (hotel_id) REFERENCES public.hotels(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

