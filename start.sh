#!/bin/bash

# Start MySQL
service mysql start
echo "MySQL service started."

# Initialize MySQL if necessary
if [ ! -d "/var/lib/mysql/dbname" ]; then
    echo "Initializing MySQL database..."
    mysql -u root -p$MYSQL_ROOT_PASSWORD < /docker-entrypoint-initdb.d/init.sql
    echo "MySQL database initialized."
fi

# Start MongoDB
mongod --config /etc/mongod.conf &
echo "MongoDB service started."

# Start Flask application
flask run --host=0.0.0.0 --reload

