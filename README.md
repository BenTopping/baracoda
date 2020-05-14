# baracoda

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
to run. For example, for a development environment we could use:

        FLASK_APP=baracoda
        FLASK_ENV=development
        DB_HOST=localhost
        DB_PORT=5432
        DB_USER=postgres
        DB_PASSWORD=postgres
        DB_DBNAME=baracoda_dev

1. Install the python libraries with pipenv:

        pipenv install

    If running into trouble with the  package, try: `export LDFLAGS="-L/usr/local/opt/openssl@1.1/lib"`
    and running `pipenv install` again.

1. Run the pipenv shell

        pipenv shell

1. Initialize the database and create required sequences (only needed when we change the config/settings.py):

        flask init-db

1. Start the app:

        flask run

## Routes

The following routes are available from this service:

    flask routes

    Endpoint                                Methods  Rule
    ---------------------------------       -------  -----------------------
    barcode_creation.get_last_barcode       GET      /barcodes/<prefix>/last
    barcode_creation.get_new_barcode        POST     /barcodes/<prefix>/new
    barcode_creation.get_new_barcode_group  POST     /barcodes_group/<prefix>/new?count=<number>
    static                                  GET      /static/<path:filename>

## Running the tests

Run the following command inside a pipenv shell:
```bash
python -m pytest
```

## Running linting checks

To run mypy:
```bash
python -m mypy .
```

## Development

To run migrations:
```bash
alembic upgrade head
```

### Autogenerating migrations

- Make sure your local database is up to date with last schema available (orm/sql/schema.sql)
- Perform any change in the models files located in ```baracoda/orm``` folder
- Run alembic and provide a comment to autogenerate the migration comparing with current database: 
```bash
alembic revision --autogenerate -m "Added account table"
```