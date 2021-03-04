# Baracoda

![CI python](https://github.com/sanger/baracoda/workflows/CI%20python/badge.svg)
![CI docker](https://github.com/sanger/baracoda/workflows/CI%20docker/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/sanger/baracoda/branch/develop/graph/badge.svg)](https://codecov.io/gh/sanger/baracoda)

Generate barcodes on demand

## How to set up a development environment

1. Install postgresql

        brew install postgresql

1. Configure Postgresql:

    To configure postgresql database for the project you only need to create the database and add a user
    to access it. For example, to create the databases baracoda_dev and baracoda_test and create the
    user postgres with password postgres to access them:

        (baracoda) bash-3.2$ psql
        psql (12.2)
        Type "help" for help.
        =# create database baracoda_dev;
        CREATE DATABASE
        =# create database baracoda_test;
        CREATE DATABASE
        =# create user postgres with encrypted password 'postgres';
        CREATE ROLE
        =# grant all privileges on database baracoda_dev to postgres;
        GRANT
        =# grant all privileges on database baracoda_test to postgres;
        GRANT

1. Create a `.env` file with the database and environment configuration for the environment we want
to run (see the example file .env.example). For example, for a development environment we could use:

        FLASK_APP=baracoda
        FLASK_ENV=development
        DB_HOST=localhost
        DB_PORT=5432
        DB_USER=postgres
        DB_PASSWORD=postgres
        DB_DBNAME=baracoda_dev
        SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://postgres:postgres@localhost:5432/baracoda_dev"

1. Install the python libraries with pipenv:

        pipenv install --dev

    If running into trouble with the  package, try: `export LDFLAGS="-L/usr/local/opt/openssl@1.1/lib"`
    and running `pipenv install` again.

1. Run the pipenv shell

        pipenv shell

1. **OPTIONAL** To create a new database, and create required sequences:

        flask init-db

1. Run migrations (if any):

        alembic upgrade head

1. Start the app:

        flask run

## Routes

The following routes are available from this service:

    flask routes

        Endpoint                                Methods  Rule
        --------------------------------------  -------  ----------------------------
        barcode_creation.get_last_barcode       GET      /barcodes/<prefix>/last
        barcode_creation.get_new_barcode        POST     /barcodes/<prefix>/new
        barcode_creation.get_new_barcode_group  POST     /barcodes_group/<prefix>/new
        static                                  GET      /static/<path:filename>

## Running the tests

Run the following command inside a pipenv shell:

    python -m pytest -vsx

## Running linting checks

To run mypy:

    mypy .

## Development

### Autogenerating migrations

- Make sure your local database is up to date with last schema available (orm/sql/schema.sql)
- Perform any change in the models files located in `baracoda/orm` folder
- Run alembic and provide a comment to autogenerate the migration comparing with current database:

        alembic revision --autogenerate -m "Added account table"

## Releases

#### UAT
On merging a pull request into develop, a release will be created with the tag/name `<branch>/<timestamp>`

#### PROD
Update `.release-version` with major/minor/patch. On merging a pull request into master, a release will be created with the release version as the tag/name 

