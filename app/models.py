from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Create db instance - this will be imported by app/__init__.py
db = SQLAlchemy()


class Service(db.Model):
    """Service model for engineering services"""
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(300))
    description = db.Column(db.Text)  # HTML content
    icon_class = db.Column(db.String(100))  # CSS icon class (e.g., 'fa-cube')
    image_url = db.Column(db.String(500))
    features = db.Column(db.JSON)  # List of key features
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    case_studies = db.relationship('CaseStudy', backref='service', lazy='dynamic')

    def __repr__(self):
        return f'<Service {self.title}>'


class CaseStudy(db.Model):
    """Portfolio/Case Study model"""
    __tablename__ = 'case_studies'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    client = db.Column(db.String(200))
    industry = db.Column(db.String(100))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))

    # Case study content
    challenge = db.Column(db.Text)  # Problem statement
    solution = db.Column(db.Text)  # Approach taken
    results = db.Column(db.Text)  # Outcomes achieved

    # Media
    thumbnail_url = db.Column(db.String(500))
    images = db.Column(db.JSON)  # List of image URLs

    # Additional details
    technologies = db.Column(db.JSON)  # List of tools/software used
    duration = db.Column(db.String(50))  # e.g., "3 months"

    # Display settings
    featured = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<CaseStudy {self.title}>'


class BlogPost(db.Model):
    """Blog post model"""
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(300))
    content = db.Column(db.Text)  # HTML content
    author = db.Column(db.String(100))
    thumbnail_url = db.Column(db.String(500))

    # Categorization
    category = db.Column(db.String(100), index=True)  # e.g., "FEA", "CFD", "CAD"
    tags = db.Column(db.JSON)  # List of tags

    # Display settings
    featured = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=False, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<BlogPost {self.title}>'

    def increment_views(self):
        """Increment view counter"""
        self.views += 1
        db.session.commit()


class ContactSubmission(db.Model):
    """Contact form submission model"""
    __tablename__ = 'contact_submissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    service_interest = db.Column(db.String(100))  # Selected service
    message = db.Column(db.Text, nullable=False)

    # Tracking information
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))

    # Admin fields
    status = db.Column(db.String(20), default='new')  # new, contacted, qualified, closed
    notes = db.Column(db.Text)  # Admin notes

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ContactSubmission from {self.name}>'


class NewsletterSubscriber(db.Model):
    """Newsletter subscription model"""
    __tablename__ = 'newsletter_subscribers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    unsubscribed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<NewsletterSubscriber {self.email}>'


class User(UserMixin, db.Model):
    """User model for admin authentication"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        """Set hashed password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
