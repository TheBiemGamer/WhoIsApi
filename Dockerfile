# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables to prevent writing .pyc files and ensure that Flask app runs in production mode
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

# Expose the port the app runs on (Flask default port 5000)
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "/app/whoisapi/app.py"]
