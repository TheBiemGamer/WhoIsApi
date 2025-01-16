# Use an official Python runtime as a base image
FROM python:3.13-slim

# Set environment variables to prevent writing .pyc files and ensure that Flask app runs in production mode
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory to /app inside the container
WORKDIR /app

# Install system dependencies necessary for Poetry and Flask
RUN apt-get update \
    && apt-get install -y curl build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (use a versioned install command to ensure compatibility)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure Poetry is installed correctly
RUN poetry --version

# Add Poetry to the PATH
ENV PATH="${PATH}:/root/.local/bin"

# Copy the pyproject.toml and poetry.lock files from the /whoisapi folder into /app/whoisapi in the container
COPY pyproject.toml poetry.lock* /app/

# Install dependencies via Poetry (production dependencies only)
RUN poetry install --no-dev --no-root --verbose

# Copy the entire /whoisapi folder into /app/whoisapi in the container
COPY . /app/

# Expose the port Flask will run on
EXPOSE 5000

# Set the entry point for the container to run your Flask app
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]
