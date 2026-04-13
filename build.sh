#!/usr/bin/env bash
set -o errexit

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Running database migrations..."
python init_database.py

echo "Creating admin user..."
python create_admin_user.py

echo "Build complete!"
