--====== measurement_unit ======
CREATE TABLE public.measurement_unit (
    id integer NOT NULL,
    name character(20)
);

CREATE SEQUENCE public.measurement_unit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.measurement_unit_id_seq OWNED BY public.measurement_unit.id;

--====== ingredients ======
CREATE TABLE public.ingredients (
    id integer NOT NULL,
    name character(50)
);

CREATE SEQUENCE public.ingredients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.ingredients_id_seq OWNED BY public.ingredients.id;

--====== recipe_steps ======
CREATE TABLE public.recipe_steps (
    id integer NOT NULL,
    step text,
    id_ref_recipe integer
);

CREATE SEQUENCE public.recipe_steps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.recipe_steps_id_seq OWNED BY public.recipe_steps.id;

--====== recipe_ingredients ======
CREATE TABLE public.recipe_ingredients (
    id_ref_ingredient integer NOT NULL,
    if_ref_recipe integer NOT NULL,
    quantity integer,
    id_ref_measurement_unit integer
);


--====== recipes ======
CREATE TABLE public.recipes (
    id integer NOT NULL,
    name character(50),
    preparation_time integer,
    coocking_time integer,
    description text,
    picture character(50),
    portion integer
);


CREATE SEQUENCE public.recipes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.recipes_id_seq OWNED BY public.recipes.id;

--====== users ======
CREATE TABLE public.users (
    id integer NOT NULL,
    email character(50),
    surname character(20),
    name character(20),
    password character(64)
);

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
ALTER TABLE public.users ADD CONSTRAINT users_email_unique UNIQUE (email);

--====== other ======
ALTER TABLE ONLY public.ingredients ALTER COLUMN id SET DEFAULT nextval('public.ingredients_id_seq'::regclass);
ALTER TABLE ONLY public.measurement_unit ALTER COLUMN id SET DEFAULT nextval('public.measurement_unit_id_seq'::regclass);
ALTER TABLE ONLY public.recipe_steps ALTER COLUMN id SET DEFAULT nextval('public.recipe_steps_id_seq'::regclass);
ALTER TABLE ONLY public.recipes ALTER COLUMN id SET DEFAULT nextval('public.recipes_id_seq'::regclass);
ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
ALTER TABLE ONLY public.measurement_unit
    ADD CONSTRAINT measurement_unit_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT ingredients_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.recipe_steps
    ADD CONSTRAINT recipe_steps_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.recipe_ingredients
    ADD CONSTRAINT recipe_ingredients_pkey PRIMARY KEY (id_ref_ingredient, if_ref_recipe);
ALTER TABLE ONLY public.recipes
    ADD CONSTRAINT recipes_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.recipe_ingredients
    ADD CONSTRAINT id_ref_ingredient_fk FOREIGN KEY (id_ref_ingredient) REFERENCES public.ingredients(id);
ALTER TABLE ONLY public.recipe_ingredients
    ADD CONSTRAINT id_ref_measurement_unit_fk FOREIGN KEY (id_ref_measurement_unit) REFERENCES public.measurement_unit(id) NOT VALID;
ALTER TABLE ONLY public.recipe_steps
    ADD CONSTRAINT id_ref_recipe_fk FOREIGN KEY (id_ref_recipe) REFERENCES public.recipes(id);
ALTER TABLE ONLY public.recipe_ingredients
    ADD CONSTRAINT id_ref_recipe_fk FOREIGN KEY (if_ref_recipe) REFERENCES public.recipes(id);