#!/bin/bash
# usage: sudo bash create_db.sh <database_name> <user> <password>

database=$1
user=$2
password=$3

psql -U postgres -c "CREATE DATABASE $database WITH ENCODING 'UTF8'"
psql -U postgres -c "CREATE SUPERUSER $user WITH PASSWORD '$password'"
psql -U postgres $database -c "GRANT ALL PRIVILEGES ON DATABASE $database to $user"
psql -U postgres $database -c "ALTER DATABASE $database OWNER TO $user"