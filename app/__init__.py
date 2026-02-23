from flask import Flask
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_admin import Admin
from config import config

# Import db from models to avoid duplicate instances
from app.models import db

# Initialize other extensions
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()
admin = Admin(name='Mechanical Insight Admin', template_mode='bootstrap4')


def create_app(config_name='default'):
    """Flask application factory"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    admin.init_app(app)

    # Configure login manager
    login_manager.login_view = 'admin_panel.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Import models (needed for migrations and admin)
    from app.models import User, Service, CaseStudy, BlogPost, ContactSubmission, NewsletterSubscriber

    # Add Flask-Admin model views
    from flask_admin.contrib.sqla import ModelView
    admin.add_view(ModelView(Service, db.session, name='Services'))
    admin.add_view(ModelView(CaseStudy, db.session, name='Case Studies'))
    admin.add_view(ModelView(BlogPost, db.session, name='Blog Posts'))
    admin.add_view(ModelView(ContactSubmission, db.session, name='Contact Submissions'))
    admin.add_view(ModelView(NewsletterSubscriber, db.session, name='Newsletter Subscribers'))
    admin.add_view(ModelView(User, db.session, name='Users'))

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.main import main_bp
    from app.blog import blog_bp
    from app.portfolio import portfolio_bp
    from app.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(portfolio_bp, url_prefix='/portfolio')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Template filters
    @app.template_filter('truncate_html')
    def truncate_html_filter(text, length=150):
        """Truncate HTML content while preserving tags"""
        if not text:
            return ''
        from html.parser import HTMLParser
        text = str(text)
        if len(text) <= length:
            return text
        return text[:length] + '...'

    @app.template_filter('format_date')
    def format_date_filter(date, format='%B %d, %Y'):
        """Format datetime object"""
        if date is None:
            return ''
        return date.strftime(format)

    # Context processors
    @app.context_processor
    def inject_services():
        """Make services available in all templates"""
        from app.models import Service
        services = Service.query.filter_by(is_active=True).order_by(Service.order).all()
        return dict(all_services=services)

    return app
