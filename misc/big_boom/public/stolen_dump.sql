--
-- PostgreSQL database dump
--

-- Dumped from database version 15.8 (Debian 15.8-1.pgdg120+1)
-- Dumped by pg_dump version 17.4

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

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ownership_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ownership_history (
    id integer NOT NULL,
    stone_id integer,
    owner_id integer,
    acquired_at timestamp without time zone,
    lost_at timestamp without time zone,
    method text
);


ALTER TABLE public.ownership_history OWNER TO postgres;

--
-- Name: stone_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stone_events (
    id integer NOT NULL,
    stone_id integer,
    event_time timestamp without time zone,
    event_type character varying,
    description text
);


ALTER TABLE public.stone_events OWNER TO postgres;

--
-- Name: stone_owners; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stone_owners (
    id integer NOT NULL,
    name character varying,
    species character varying,
    affiliation character varying
);


ALTER TABLE public.stone_owners OWNER TO postgres;

--
-- Name: stones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stones (
    id integer NOT NULL,
    code_hash character varying,
    color character varying,
    power_description text,
    first_appearance character varying
);


ALTER TABLE public.stones OWNER TO postgres;

--
-- Data for Name: ownership_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ownership_history (id, stone_id, owner_id, acquired_at, lost_at, method) FROM stdin;
1	1	1	2000-01-01 00:00:00	2002-03-21 00:00:00	Discovered in ruins
2	1	5	2002-03-21 00:00:00	2010-10-10 00:00:00	Traded under mysterious circumstances
3	1	4	2010-10-10 00:00:00	\N	Stolen during a galactic heist
4	2	2	2001-02-11 00:00:00	2004-08-16 00:00:00	Inherited from predecessor
5	2	6	2004-08-16 00:00:00	2011-07-04 00:00:00	Lost in battle
6	2	8	2011-07-04 00:00:00	\N	Integrated into AI core
7	3	3	1998-05-24 00:00:00	2005-03-11 00:00:00	Uncovered beneath frozen sea
8	3	10	2005-03-11 00:00:00	2018-09-09 00:00:00	Gifted during alliance
9	3	7	2018-09-09 00:00:00	\N	Won in contest
10	4	6	1969-07-20 00:00:00	2001-09-10 00:00:00	Seized from enemy
11	4	9	2001-09-10 00:00:00	2008-12-24 00:00:00	Used in experiment
12	4	3	2008-12-24 00:00:00	\N	Recovered after chaos event
13	5	7	2003-04-22 00:00:00	2006-06-17 00:00:00	Found in ancient temple
14	5	1	2006-06-17 00:00:00	2014-11-01 00:00:00	Passed through secret auction
15	5	2	2014-11-01 00:00:00	\N	Acquired by subterfuge
16	6	8	2000-12-31 00:00:00	2005-05-05 00:00:00	Synthesized in lab
17	6	5	2005-05-05 00:00:00	2012-08-20 00:00:00	Taken during uprising
18	6	10	2012-08-20 00:00:00	\N	Inherited as legacy
\.


--
-- Data for Name: stone_events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stone_events (id, stone_id, event_time, event_type, description) FROM stdin;
1	1	2002-03-21 00:00:00	Trade	Stone exchanged in secret between Maddox and Kronos.
2	2	2004-08-16 00:00:00	Battle Loss	Vex captured the stone from Artemis.
3	3	2005-03-11 00:00:00	Gift	Nova Corps received stone as a diplomatic gesture.
4	4	2001-09-10 00:00:00	Experiment	Iris used the stone to attempt energy manipulation.
5	5	2006-06-17 00:00:00	Auction	Stone passed hands at a covert auction held by Kronos.
6	6	2005-05-05 00:00:00	Uprising	Vex took the stone during rebellion in the capital.
\.


--
-- Data for Name: stone_owners; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stone_owners (id, name, species, affiliation) FROM stdin;
1	Kronos	Eternal	Celestials
2	Artemis	Human	Order of Shadows
3	Bor	Asgardian	Ancient Asgard
4	Zyra	Synthetic	Guardians
5	Maddox	Human	Wanderers
6	Vex	Unknown	Rogues
7	Sol	Human	Seekers
8	Hex	AI	None
9	Iris	Mutant	Shadows
10	Nova	Energy Being	Nova Corps
\.


--
-- Data for Name: stones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stones (id, code_hash, color, power_description, first_appearance) FROM stdin;
4	6953250040028	Blue	Enables alteration of the physical laws and structure of matter.	Doctor Strange
2	193433130	Purple	Enables traversal between distant points instantly.	Thor: The Dark World
5	6383401807	Red	Empowers the wielder with unmatched destructive capability.	The Avengers
1	6385415121	Amber	Allows the user to influence causality and manipulate events.	Guardians of the Galaxy
6	210722229252	Yellow	Gives the ability to control the flow and perception of time.	Captain America: The First Avenger
3	210654488433	Green	Controls the very essence of consciousness and perception.	Avengers: Infinity War
\.


--
-- Name: ownership_history ownership_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ownership_history
    ADD CONSTRAINT ownership_history_pkey PRIMARY KEY (id);


--
-- Name: stone_events stone_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stone_events
    ADD CONSTRAINT stone_events_pkey PRIMARY KEY (id);


--
-- Name: stone_owners stone_owners_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stone_owners
    ADD CONSTRAINT stone_owners_pkey PRIMARY KEY (id);


--
-- Name: stones stones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stones
    ADD CONSTRAINT stones_pkey PRIMARY KEY (id);


--
-- Name: ownership_history ownership_history_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ownership_history
    ADD CONSTRAINT ownership_history_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.stone_owners(id);


--
-- Name: ownership_history ownership_history_stone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ownership_history
    ADD CONSTRAINT ownership_history_stone_id_fkey FOREIGN KEY (stone_id) REFERENCES public.stones(id);


--
-- Name: stone_events stone_events_stone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stone_events
    ADD CONSTRAINT stone_events_stone_id_fkey FOREIGN KEY (stone_id) REFERENCES public.stones(id);


--
-- PostgreSQL database dump complete
--

