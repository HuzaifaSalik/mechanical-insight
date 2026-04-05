"""Test configuration and fixtures"""
import pytest
from app import create_app, db as _db
from app.models import User, Service, BlogPost, ContactSubmission, NewsletterSubscriber, CaseStudy


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    app = create_app('testing')
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def db(app):
    """Create database for testing"""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.rollback()
        _db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def sample_user(db):
    """Create a sample user for testing"""
    user = User(
        username='testadmin',
        email='admin@test.com',
        is_admin=True
    )
    user.set_password('testpass123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def sample_service(db):
    """Create a sample service for testing"""
    service = Service(
        title='Test Service',
        slug='test-service',
        short_description='A test service',
        description='Full description of test service',
        icon='fa-cogs',
        is_active=True,
        order=1
    )
    db.session.add(service)
    db.session.commit()
    return service


@pytest.fixture
def sample_blog_post(db):
    """Create a sample blog post for testing"""
    post = BlogPost(
        title='Test Blog Post',
        slug='test-blog-post',
        content='This is test blog content',
        category='engineering',
        is_published=True
    )
    db.session.add(post)
    db.session.commit()
    return post


@pytest.fixture
def sample_contact(db):
    """Create a sample contact submission"""
    contact = ContactSubmission(
        name='John Doe',
        email='john@test.com',
        message='Test message',
        status='new'
    )
    db.session.add(contact)
    db.session.commit()
    return contact
