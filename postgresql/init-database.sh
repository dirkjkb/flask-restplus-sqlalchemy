#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER docker WITH PASSWORD 'password';
    CREATE DATABASE flask;
    GRANT ALL PRIVILEGES ON DATABASE flask TO docker, postgres;
EOSQL