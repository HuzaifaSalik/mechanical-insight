"""Create an admin user for the Company Insight website"""
import sys
from app import create_app, db
from app.models import User

# Create Flask app
app = create_app('development')

with app.app_context():
    # Check if admin user already exists
    existing_admin = User.query.filter_by(username='admin').first()

    if existing_admin:
        print('Admin user already exists!')
        print(f'Username: {existing_admin.username}')
        print(f'Email: {existing_admin.email}')
        sys.exit(0)

    # Create new admin user
    admin = User(
        username='admin',
        email='admin@companyinsight.com',
        is_admin=True
    )
    admin.set_password('admin123')

    try:
        db.session.add(admin)
        db.session.commit()
        print('\n[SUCCESS] Admin user created successfully!')
        print('\nLogin credentials:')
        print('  Username: admin')
        print('  Password: admin123')
        print('  Email: admin@companyinsight.com')
        print('\nYou can now login at: http://localhost:5000/admin/login')
        print('\nIMPORTANT: Change the password after first login!')
    except Exception as e:
        print(f'Error creating admin user: {e}')
        db.session.rollback()
        sys.exit(1)
