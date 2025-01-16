# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and to disable output buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app

# Set environment variable for Flask to know the app's entry point
ENV FLASK_APP=whoisapi/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port Flask runs on (default is 5000)
EXPOSE 5000

# Command to run the Flask app using flask run
CMD ["flask", "run"]
