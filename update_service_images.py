"""Update service images in the database"""
import sys
from app import create_app, db
from app.models import Service

# Create Flask app
app = create_app('development')

with app.app_context():
    # Mapping of services to image filenames
    service_images = {
        'product-design-cad': '/static/images/portfolio/cad-model.jpg',  # Image 1
        'manufacturing-analysis': '/static/images/portfolio/manufacturing-fea.jpg',  # Image 2
        'cfd-simulations': '/static/images/portfolio/cfd-analysis.jpg',  # Image 3
        'aerospace-uav': '/static/images/portfolio/aerodynamic-cfd.jpg',  # Image 4
        'automotive-simulations': '/static/images/portfolio/automotive-cfd.jpg',  # Image 5
        'mechanical-design-fea': '/static/images/portfolio/fea-analysis.jpg',  # Image 6
    }

    print('Updating service images...')

    for slug, image_url in service_images.items():
        service = Service.query.filter_by(slug=slug).first()
        if service:
            service.image_url = image_url
            print(f'  Updated: {service.title} -> {image_url}')
        else:
            print(f'  Not found: {slug}')

    try:
        db.session.commit()
        print('\n[SUCCESS] Service images updated!')
        print('\nNOTE: Make sure to save your images in the following locations:')
        for slug, image_url in service_images.items():
            print(f'  - c:\\New folder\\app{image_url}')
    except Exception as e:
        print(f'Error updating services: {e}')
        db.session.rollback()
        sys.exit(1)
