#!/bin/bash

# set -e : Exit if a command returns a non-zero status.
# set -x : Display debugging output.
set -ex

# Get the absolute path of this script.
SCRIPT_DIR=$(cd $(dirname $0); pwd)

# Get the absolute path of the project root.
ROOT_DIR=$(cd $(dirname $0)/..; pwd)

cd $ROOT_DIR

# For PostgreSQL, we do not need to remove a local SQLite database file.
# If needed, you can add commands to drop and recreate the PostgreSQL database here.

# Run migration using Alembic.
alembic upgrade head

# Create initial users.
PASSWD="admin"
python api/manage.py create-user sys_admin -r SYSTEM_ADMIN -p $PASSWD
python api/manage.py create-user loc_admin -r LOCATION_ADMIN -p $PASSWD
python api/manage.py create-user loc_operator -r LOCATION_OPERATOR -p $PASSWD