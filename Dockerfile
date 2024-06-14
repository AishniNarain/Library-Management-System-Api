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


# # Use an official Python runtime as a parent image
# FROM python:3.11-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install dependencies
# RUN apt-get update && apt-get install -y \
#     wget \
#     gnupg \
#     supervisor \
#     libaio1 \
#     libncurses5 \
#     curl \
#     xz-utils \
#     libnuma1

# # Install MySQL from tarball
# RUN wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.28-linux-glibc2.12-x86_64.tar.xz && \
#     tar -xvf mysql-8.0.28-linux-glibc2.12-x86_64.tar.xz && \
#     mv mysql-8.0.28-linux-glibc2.12-x86_64 /usr/local/mysql && \
#     ln -s /usr/local/mysql/bin/* /usr/local/bin/ && \
#     mkdir /usr/local/mysql/mysql-files && \
#     chmod 750 /usr/local/mysql/mysql-files && \
#     useradd -r -s /bin/false mysql && \
#     chown -R mysql:mysql /usr/local/mysql && \
#     /usr/local/mysql/bin/mysqld --initialize-insecure --user=mysql && \
#     /usr/local/mysql/bin/mysql_ssl_rsa_setup && \
#     chown -R mysql:mysql /usr/local/mysql/mysql-files

# # Add MongoDB GPG key and repository
# RUN curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add - && \
#     echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list

# # Update package list again
# RUN apt-get update

# # Manually install libssl1.1 from an alternative source
# RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
#     dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
#     rm libssl1.1_1.1.1f-1ubuntu2_amd64.deb

# # Install MongoDB
# RUN apt-get install -y mongodb-org=4.4.18 mongodb-org-server=4.4.18 mongodb-org-shell=4.4.18 mongodb-org-mongos=4.4.18 mongodb-org-tools=4.4.18

# # Clean up
# RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Create necessary directories
# RUN mkdir -p /var/log/supervisor /data/db /var/lib/mysql

# # Create supervisor configuration file
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# # Environment variables
# ENV FLASK_ENV=development
# # Expose the ports
# EXPOSE 5000 3306 27017

# # Command to run supervisor
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]


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

RUN sed -i 's/bind-address\s*=.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code and Supervisor configuration
COPY . /app
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


# Run Supervisor
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]


# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0


# Expose ports
EXPOSE 5000 3306 27017

# # Run app.py when the container launches using flask command as below
# # CMD ["wait-for-it.sh", "mysql-db:3306", "--", "wait-for-it.sh", "mongo-db:27017", "--", "flask", "run", "--reload"]
CMD ["flask", "run", "--reload"]
