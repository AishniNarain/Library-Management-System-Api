# # Use an official Python runtime as a parent image
# FROM python:3.11-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # COPY wait-for-it.sh /usr/local/bin/
# # RUN chmod +x /usr/local/bin/wait-for-it.sh

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Make port 5000 available to the world outside this container
# EXPOSE 5000

# # Set environment variables for Flask
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

# # Run app.py when the container launches using flask command as below
# # CMD ["wait-for-it.sh", "mysql-db:3306", "--", "wait-for-it.sh", "mongo-db:27017", "--", "flask", "run", "--reload"]
# CMD ["flask", "run", "--reload"]

# Use an official Ubuntu runtime as a parent image
FROM ubuntu:20.04

# Set the working directory in the container
WORKDIR /app

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && \
    apt-get install -y \
        mysql-server \
        supervisor \
        python3 \
        python3-pip \
        curl \
        gnupg && \
    rm -rf /var/lib/apt/lists/*

# Install MongoDB
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add - && \
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list && \
    apt-get update && \
    apt-get install -y mongodb-org=4.4.18 mongodb-org-server=4.4.18 mongodb-org-shell=4.4.18 mongodb-org-mongos=4.4.18 mongodb-org-tools=4.4.18 && \
    rm -rf /var/lib/apt/lists/*

# Create MongoDB data directory
RUN mkdir -p /data/db && chown -R mongodb:mongodb /data/db

# Copy MongoDB configuration file
COPY mongod.conf /etc/mongod.conf

# RUN sed -i 's/bind-address\s*=.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf

# Adjust MySQL configuration to bind to all interfaces and increase timeout settings
RUN sed -i 's/bind-address\s*=.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf && \
    echo "[mysqld]\nwait_timeout = 28800\ninteractive_timeout = 28800\n" >> /etc/mysql/mysql.conf.d/mysqld.cnf


# ENV MYSQL_ROOT_PASSWORD=MYSQL_ROOT_PASSWORD

# Copy SQL dump and initialization scripts
COPY library_data.sql /docker-entrypoint-initdb.d/
COPY init.sql /docker-entrypoint-initdb.d/

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code and Supervisor configuration
COPY . /app
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# # Copy wait-for-it script to wait for MySQL and MongoDB to be ready
# COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
# RUN chmod +x /usr/local/bin/wait-for-it.sh


# Set environment variables for Flask
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

# Expose ports
EXPOSE 5000 3306 27017

# # Run app.py when the container launches using flask command as below
# # CMD ["wait-for-it.sh", "mysql-db:3306", "--", "wait-for-it.sh", "mongo-db:27017", "--", "flask", "run", "--reload"]
# CMD ["flask", "run", "--reload"]
# CMD mysqld & \
#     mongod --config /etc/mongod.conf & \
#     flask run --host=0.0.0.0 --reload

# # Script to start all services
# COPY start.sh /start.sh
# RUN chmod +x /start.sh

# # Start all services
# CMD ["/start.sh"]


COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

# Run Supervisor
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
