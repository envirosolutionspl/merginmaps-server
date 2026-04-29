CREATE TABLE public.login_attempts (
	id serial4 NOT NULL,
	user_id int4 NOT NULL,
	password_correct bool NOT NULL,
	CONSTRAINT login_attempts_pkey PRIMARY KEY (id)
);