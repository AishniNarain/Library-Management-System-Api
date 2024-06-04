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

# FROM python:latest

# Install dependencies and add MongoDB repository
# RUN apt-get update && \
#     apt-get install -y gnupg wget lsb-release curl && \
#     wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add - && \
#     CODENAME=$(lsb_release -cs) && \
#     echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $CODENAME/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list && \
#     apt-get update && \
#     apt-get install -y mysql-server mongodb-org supervisor

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

# # Install supervisord
# RUN apt-get update && apt-get install -y supervisor

# # Copy the supervisord configuration file
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# # Expose ports for MySQL and MongoDB
# EXPOSE 3306 27017

# # Command to run supervisord
# CMD ["/usr/bin/supervisord"]





# # Use an official Python runtime as a parent image
# FROM python:3.9-slim

# # Set environment variables
# ENV MYSQL_ROOT_PASSWORD=rootpassword
# ENV MYSQL_DATABASE=dbname
# ENV FLASK_APP = app.py
# ENV FLASK_RUN_HOST=0.0.0.0

# # Copy the current directory contents into the container at /app
# WORKDIR /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Install supervisord
# RUN apt-get update && apt-get install -y supervisor

# # Copy supervisor configuration
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# # Expose the service ports
# EXPOSE 5000 3306 27017

# # Start supervisord
# CMD ["/usr/bin/supervisord"]



# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    gnupg \
    wget \
    lsb-release \
    supervisor

# Add MySQL APT repository and install MySQL server
RUN wget https://dev.mysql.com/get/mysql-apt-config_0.8.16-1_all.deb && \
    DEBIAN_FRONTEND=noninteractive dpkg -i mysql-apt-config_0.8.16-1_all.deb && \
    apt-get update && \
    apt-get install -y mysql-server

# Add MongoDB APT repository and install MongoDB
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add - && \
    echo "deb http://repo.mongodb.org/apt/debian $(lsb_release -sc)/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list && \
    apt-get update && \
    apt-get install -y mongodb-org

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Environment variables
ENV FLASK_ENV=development
ENV DATABASE_URL=mysql+pymysql://root:rootpassword@localhost:3306/dbname
ENV MONGO_URI=mongodb://localhost:27017/

# Expose the ports
EXPOSE 5000 3306 27017

# Command to run supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
