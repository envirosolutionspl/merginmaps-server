# Mergin web-app

Monorepo for mergin frontend stuff:

- web application [./packages/app](./packages/app)
- admin web application [./packages/app](./packages/admin-app)

# Monorepo Structure

* this projects uses yarn workspaces
* monorepo consists of root directory with own package.json and individual workspaces in `packages` directory
* root package.json defines common devDependencies and it cannot hold any non-development dependency
* individual workspace package.json defines dependencies used in that particular workspace package
* frontend application (e.g. app) is also a workspace package (@mergin/app) held in directory [./packages/app](./packages/app).

Application constist of several packages in `packages` directory:

- @mergin/lib - Shared library for common features
- @mergin/admin-lib - Shared library for admin
- @mergin/app - Web appliacation"
- @mergin/admin-app - Web application for administration

Library packages with *-lib* name are containing shared code for *-app* applications.

Web application *@mergin/app* is using shared library *@mergin/lib*. Web application for administration *admin-app* is using shared library *@mergin/admin-lib*.

## Environment variables

The frontend packages use package-level `.env` files loaded by Vite:

- [./packages/app/.env](./packages/app/.env)
- [./packages/admin-app/.env](./packages/admin-app/.env)
- [./packages/lib/.env](./packages/lib/.env)
- [./packages/admin-lib/.env](./packages/admin-lib/.env)

`VITE_LANG` sets the default frontend language. Public Weblate settings are
provided with `VITE_WEBLATE_URL`, `VITE_WEBLATE_PROJECT`,
`VITE_WEBLATE_COMPONENT` and `VITE_WEBLATE_TIMEOUT_MS`. `VITE_WEBLATE_URL`
should normally point to the same-origin `/weblate` proxy. These values are
public frontend configuration and must not contain secrets.

Dynamic translations are fetched from Weblate by the frontend through the Vite
dev proxy or the production nginx proxy. Missing or unavailable translations
fall back to the local English messages in
[./packages/lang/translations/EN.ts](./packages/lang/translations/EN.ts).
The production nginx proxy reads the upstream Weblate domain from
`WEBLATE_HOST` in the root `.prod.env`.

For details about development follow instructions in [development guide](../development.md).
