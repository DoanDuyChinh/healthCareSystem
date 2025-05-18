#!/bin/bash

# Create necessary directories
mkdir -p static/css
mkdir -p static/js
mkdir -p static/img
mkdir -p media/profile_pics
mkdir -p media/lab_results

# Move style.css to static directory
cp templates/style.css static/css/style.css

# Remove style.css from templates
rm templates/style.css

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "SECRET_KEY=your-secret-key-here" > .env
    echo "DEBUG=True" >> .env
    echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env
fi

# Create database directory if using SQLite
mkdir -p data

# Set permissions
chmod +x entrypoint.sh

echo "Setup completed successfully."
