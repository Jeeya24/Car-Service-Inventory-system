#!/bin/bash

echo "Setting up Car Inventory Management System..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "Please edit .env file with your database credentials"
fi

echo "Setup complete!"
echo "1. Edit .env file with your database credentials"
echo "2. Run: mysql -u root -p < fix_database.sql"
echo "3. Run: mysql -u root -p < add_time_fields.sql"
echo "4. Run: python3 app.py"