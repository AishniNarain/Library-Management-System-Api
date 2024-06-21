#!/bin/bash

# Start MySQL service
service mysql start

# Run initialization scripts
mysql < /docker-entrypoint-initdb.d/init.sql

# Start MongoDB service
service mongo start
# mongod --fork --logpath /var/log/mongodb.log --config /etc/mongod.conf

# Start Flask
# flask run --host=0.0.0.0 --reload

#Run supervisor
# exec supervisord -c /etc/supervisor/conf.d/supervisord.conf

exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf