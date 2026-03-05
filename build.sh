#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database migrations
flask db upgrade

# Seed services if they don't exist
python -c "
from app import create_app, db
from app.models import Service
import os

app = create_app(os.getenv('FLASK_ENV', 'production'))
with app.app_context():
    # Check if services exist
    if Service.query.count() == 0:
        print('Seeding services...')
        os.system('flask seed_services')
    else:
        print('Services already exist, skipping seed.')
"
