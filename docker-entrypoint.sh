set -e
service postgresql start
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER docker;
    CREATE DATABASE dev;
    GRANT ALL PRIVILEGES ON DATABASE dev TO docker;
EOSQL
