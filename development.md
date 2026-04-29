
# Mergin Maps Development guide

This page contains useful information for those who wish to develop Mergin.

## Running locally (for dev)
Install dependencies and run services:

### Postgres and Redis

```shell
$ docker run -d --rm --name mergin_maps_dev_db -p 5002:5432 -e POSTGRES_PASSWORD=postgres postgres:14
$ docker run -d --rm --name mergin_maps_dev_redis -p 6379:6379 redis
```

### Server
```shell
$ pip3 install pipenv
$ cd server
# Install dependencies with pipenv
# Note: You can append --three flag in older versions of pipenv (< 3.16.8 2023-02-04)
$ pipenv install --dev
$ export FLASK_APP=application; export COLLECT_STATISTICS=0
$ pipenv run flask init-db
# create admin user
$ pipenv run flask user create admin topsecret --is-admin --email admin@example.com
# create (non admin) user
$ pipenv run flask user create user topsecret --email user@example.com
$ pipenv run celery -A application.celery worker --loglevel=info &
$ pipenv run flask run # run dev server on port 5000
```

### Web applications

Before installing the web applications, make sure you have Node.js installed in a supported version. The applications require Node.js version **18 or higher**.

```shell
$ cd web-app
$ yarn install
$ yarn link:dependencies # link dependencies
$ yarn build:libs # bild libraries @mergin/lib @mergin/admin-lib @mergin/lib-vue2
$ yarn dev  # development client web application dev server on port 8080 (package @mergin/app)
$ yarn dev:admin  # development admin appplication dev server on port 8081 (package @mergin/admin-app)
```

Frontend applications read Vite environment variables from their package `.env`
files. Keep the same public frontend values in the app and library packages
when running both applications locally:

```shell
web-app/packages/app/.env
web-app/packages/admin-app/.env
web-app/packages/lib/.env
web-app/packages/admin-lib/.env
```

The default language is configured with `VITE_LANG`:

```shell
VITE_LANG=PL
```

Production nginx uses `WEBLATE_HOST` from `.prod.env` for the Weblate proxy:

```shell
WEBLATE_HOST=weblate.enviro-dev.pl
```

When overriding `WEBLATE_HOST` in `.prod.env`, pass `.prod.env` to Docker
Compose as the compose environment file, for example:

```shell
docker-compose --env-file .prod.env -f prod.yml up
```

The compose files require `WEBLATE_HOST` to be provided by `.prod.env` or the
shell environment; there is no Weblate domain fallback in the compose files.

Dynamic frontend translations are loaded from a public Weblate component through
the same-origin `/weblate` proxy. The Weblate configuration is public and does
not contain secrets:

```shell
VITE_WEBLATE_URL=/weblate
VITE_WEBLATE_PROJECT=mergin-maps
VITE_WEBLATE_COMPONENT=frontend
VITE_WEBLATE_TIMEOUT_MS=1000
```

The development Vite server proxies `/weblate` when `WEBLATE_HOST` or
`WEBLATE_PROXY_TARGET` is provided before running `yarn dev` or
`yarn dev:admin`.
Production docker/nginx deployments proxy the same `/weblate` path in
`nginx.conf`.

If Weblate is not configured or cannot be reached, the frontend falls back to
the local English translations from `web-app/packages/lang/translations/EN.ts`.
Restart `yarn dev` or `yarn dev:admin` after changing any `.env` value.

If you are developing a library package (named **-lib*), it is useful to watch the library for changes instead of rebuilding it each time. 

To watch the @mergin/lib library while developing:

```shell
# watch:admin-lib, etc.
yarn watch:lib
# Also watch type definitions
yarn watch:lib:types
```

Watching the type definitions is also useful to pick up any changes to imports or new components that are added.


## Running tests
To launch the unit tests run:
```shell
$ docker run -d --rm --name testing_pg -p 5435:5432 -e POSTGRES_PASSWORD=postgres postgres:14
$ cd server
$ pipenv install --dev --sequential --verbose
$ pipenv run pytest -v --cov=mergin mergin/tests
```
