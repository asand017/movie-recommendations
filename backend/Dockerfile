# Use the official Python image from the Docker Hub
FROM python:3.13-rc-slim

# Install the PostgreSQL development & other dependent libraries
RUN apt-get update && \
    apt-get install -y libpq-dev gcc g++ python3-dev libffi-dev && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
