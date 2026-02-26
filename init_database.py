"""Initialize the database and seed services"""
import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Service

# Create Flask app
app = create_app('development')

with app.app_context():
    # Create all tables
    print('Creating database tables...')
    db.create_all()
    print('Database tables created!')

    # Seed services
    print('Seeding services...')

    services_data = [
        {
            'slug': 'product-design-cad',
            'title': 'Product Design & CAD Modeling',
            'subtitle': 'Transform your ideas into precise 3D models',
            'description': '<p>Our expert team delivers comprehensive CAD modeling services for product development, from initial concept to manufacturing-ready designs.</p>',
            'icon_class': 'fa-cube',
            'order': 1,
            'is_active': True
        },
        {
            'slug': 'mechanical-design-fea',
            'title': 'Mechanical Design & Structural Analysis (FEA)',
            'subtitle': 'Optimize your designs with advanced finite element analysis',
            'description': '<p>Comprehensive structural analysis services to ensure your products meet safety and performance requirements.</p>',
            'icon_class': 'fa-vector-square',
            'order': 2,
            'is_active': True
        },
        {
            'slug': 'automotive-simulations',
            'title': 'Automotive & Transportation Simulations',
            'subtitle': 'Advanced simulations for the automotive industry',
            'description': '<p>Specialized simulation services for automotive components and systems, from crashworthiness to NVH analysis.</p>',
            'icon_class': 'fa-car',
            'order': 3,
            'is_active': True
        },
        {
            'slug': 'aerospace-uav',
            'title': 'Aerospace & UAV Engineering Support',
            'subtitle': 'Cutting-edge solutions for aerospace applications',
            'description': '<p>Expert engineering support for aerospace and UAV projects, including aerodynamic analysis and structural optimization.</p>',
            'icon_class': 'fa-plane',
            'order': 4,
            'is_active': True
        },
        {
            'slug': 'manufacturing-analysis',
            'title': 'Manufacturing & Industrial Equipment Analysis',
            'subtitle': 'Optimize your manufacturing processes',
            'description': '<p>Comprehensive analysis services for manufacturing equipment and industrial machinery to improve efficiency and reliability.</p>',
            'icon_class': 'fa-industry',
            'order': 5,
            'is_active': True
        },
        {
            'slug': 'cfd-simulations',
            'title': 'Computational Fluid Dynamics (CFD) Simulations',
            'subtitle': 'Advanced fluid flow analysis and optimization',
            'description': '<p>State-of-the-art CFD simulations for fluid flow, heat transfer, and multiphase flow applications.</p>',
            'icon_class': 'fa-water',
            'order': 6,
            'is_active': True
        },
        {
            'slug': 'thermal-analysis',
            'title': 'Thermal & Heat Transfer Analysis',
            'subtitle': 'Thermal management solutions for complex systems',
            'description': '<p>Comprehensive thermal analysis services to optimize heat dissipation and thermal management in your products.</p>',
            'icon_class': 'fa-fire',
            'order': 7,
            'is_active': True
        }
    ]

    # Simply add all services (ignore duplicates)
    for service_data in services_data:
        try:
            service = Service(**service_data)
            db.session.add(service)
            print(f'  Added: {service_data["title"]}')
        except Exception as e:
            print(f'  Skipped (error): {service_data["title"]} - {e}')
            db.session.rollback()

    try:
        db.session.commit()
    except Exception as e:
        print(f'Error committing services: {e}')
        db.session.rollback()
    print('Services seeded successfully!')
    print('\n[SUCCESS] Database initialization complete!')
    print('You can now run the application with: python run.py')
