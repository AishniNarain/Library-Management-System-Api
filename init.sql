-- Create a new user
CREATE USER 'remote_user'@'172.17.0.1' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'remote_user'@'172.17.0.1';
FLUSH PRIVILEGES;

CREATE DATABASE dbname;

USE dbname;

-- Load your initial data
SOURCE /docker-entrypoint-initdb.d/library_data.sql;
