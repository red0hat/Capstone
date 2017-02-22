CREATE TABLE public.page
(
    page_id integer NOT NULL,
    title character varying(127) COLLATE pg_catalog."default",
    created_at timestamp without time zone DEFAULT now(),
    page text COLLATE pg_catalog."default",
    CONSTRAINT page_pkey PRIMARY KEY (page_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.page
    OWNER to chris;

CREATE TABLE public.category
(
    category_id integer NOT NULL,
    category_name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT category_pkey PRIMARY KEY (category_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.category
    OWNER to chris;

CREATE TABLE public.page_cate
(
    page_id integer NOT NULL,
    category_id integer NOT NULL,
    CONSTRAINT pk_page_cate PRIMARY KEY (category_id, page_id),
    CONSTRAINT page_cate_category_id_fkey FOREIGN KEY (category_id)
        REFERENCES public.category (category_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT page_cate_page_id_fkey FOREIGN KEY (page_id)
        REFERENCES public.page (page_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.page_cate
    OWNER to chris;

CREATE TABLE public.page_vec
(
    page_id integer NOT NULL,
    page_vector double precision[] NOT NULL,
    CONSTRAINT pk_page_vec PRIMARY KEY (page_id),
    CONSTRAINT fk_page_vec FOREIGN KEY (page_id)
        REFERENCES public.page (page_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.page_vec
    OWNER to chris;

CREATE TABLE public.cate_vec
(
    category_id integer NOT NULL,
    category_vec double precision[] NOT NULL,
    CONSTRAINT category_vec_pkey PRIMARY KEY (category_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.cate_vec
    OWNER to chris;