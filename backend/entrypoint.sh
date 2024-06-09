#!/bin/sh

# Check if the migrations directory exists
if [ ! -d "migrations" ]; then
  echo "Migrations directory not found. Initializing migrations..."
  flask db init
fi

# Generate a migration script
flask db migrate -m "Initial migration" || true

# Apply the migration
flask db upgrade

# Start the application
exec gunicorn -w 1 --threads 2 --timeout 120 -b 0.0.0.0:5000 wsgi:app