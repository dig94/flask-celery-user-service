FROM python:3.9-slim

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    gcc

RUN apt update
RUN apt upgrade -y
# Set the working directory in the container
# WORKDIR /app

# COPY . /app
COPY . .
# Install any Python dependencies
RUN pip install Cython
RUN pip install -r requirements.txt

# Expose any necessary ports (e.g., if you have a web app)
EXPOSE 5001

# Command to run the application (adjust based on your app's entry point)
CMD python app.py


