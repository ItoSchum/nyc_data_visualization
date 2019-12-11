--
-- (Jiarui Jiang) and (Yitao Shen) finall project
--
--
-- PostgreSQL database dump
-- Dumped from database version 9.6.5
-- Dumped by pg_dump version 9.6.5

DROP TABLE IF EXISTS airquality CASCADE;
DROP TABLE IF EXISTS airquality_indicator CASCADE;
DROP TABLE IF EXISTS airquality_geo CASCADE;
DROP TABLE IF EXISTS crime CASCADE;
DROP TABLE IF EXISTS crime_desc CASCADE;
DROP TABLE IF EXISTS crime_geo CASCADE;
DROP TABLE IF EXISTS crime_region CASCADE;
DROP TABLE IF EXISTS abnyc CASCADE;
DROP TABLE IF EXISTS abnyc_geo CASCADE;
DROP TABLE IF EXISTS abnyc_nbhd CASCADE;
DROP TABLE IF EXISTS abnyc_host CASCADE;
DROP TABLE IF EXISTS liquor CASCADE;
DROP TABLE IF EXISTS liquor_geo CASCADE;
DROP TABLE IF EXISTS liquor_type CASCADE;


--
-- Name: airquality; Type: TABLE; Schema: public; Owner: newyork
--

CREATE TABLE airquality(
    indicator_data_id integer,
    indicator_id integer,
    name character varying(255),
    measure character varying(255),
    year_description character varying(255),
    data_valuemessage float
);

CREATE TABLE airquality_indicator(
	indicator_id integer,
	indicator_name character varying(255)
);

CREATE TABLE airquality_geo(
	indicator_data_id integer,
	geo_type_name character varying(255),
    geo_entity_id integer,
    geo_entity_name character varying(255)
);


--
-- Name: crime; Type: TABLE; Schema: public; Owner: newyork
--

CREATE TABLE crime(
    cmplnt_num integer,
    cmplnt_fr_dt date,
    cmplnt_fr_tm time,
    ky_cd integer,
    loc_of_occur_desc character varying(255),
    prem_typ_desc character varying(255)
    
);

CREATE TABLE crime_desc(
	ky_cd integer,
    ofns_desc character varying(255),
	law_cat_cd character varying(255)
);

CREATE TABLE crime_geo(
	cmplnt_num integer,
	latitude float,
	longitude float
);

CREATE TABLE crime_region(
    cmplnt_num integer,
    boro_nm character varying(255)
);


--
-- Name: abnyc; Type: TABLE; Schema: public; Owner: newyork
--

CREATE TABLE abnyc (
    id INTEGER,
    name CHARACTER VARYING(255),
    host_id CHARACTER VARYING(255),
    neighbourhood CHARACTER VARYING(255),
    room_type CHARACTER VARYING(255),
    price integer,
    minimum_nights integer,
    number_of_reviews integer,
    last_review DATE,
    reviews_per_month float,
    calculated_host_listings_count integer,
    availability_365 integer
);

CREATE TABLE abnyc_geo(
    id INTEGER,
	latitude float,
    longitude float
);

CREATE TABLE abnyc_nbhd(
	neighbourhood_group CHARACTER VARYING(255),
    neighbourhood CHARACTER VARYING(255)
);

CREATE TABLE abnyc_host(
	host_id INTEGER,
	host_name CHARACTER VARYING(255)
);



--
-- Name: Liquor; Type: TABLE; Schema: public; Owner: newyork
--

CREATE TABLE liquor (
    license_serial_number integer,
    license_class_code integer,
    premises_name CHARACTER VARYING(255),
    doing_business_as CHARACTER VARYING(255),
    license_certificate_number integer,
    license_original_issue_date DATE,
    license_effective_date DATE,
    license_expiration_date DATE
);

CREATE TABLE liquor_geo(
	license_serial_number integer,
	latitude float,
    longitude float
);

CREATE TABLE liquor_type(
	license_class_code integer,
	license_type_name CHARACTER VARYING(255)
);
