# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install the PostgreSQL development libraries, build tools, and libffi-dev
RUN apt-get update && \
    apt-get install -y libpq-dev gcc g++ python3-dev libffi-dev && \
    apt-get clean

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml file into the container
COPY pyproject.toml .

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "-w", "1","--threads", "2", "--timeout", "120", "-b", "0.0.0.0:5001", "wsgi:app"]