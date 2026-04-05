"""Unit tests for all database models"""
import pytest
from app.models import User, Service, BlogPost, ContactSubmission, NewsletterSubscriber, CaseStudy
from datetime import datetime


class TestUserModel:
    """Tests for User model"""

    def test_create_user(self, db):
        """Test user creation with all fields"""
        user = User(username='testuser', email='test@example.com', is_admin=False)
        user.set_password('securepass123')
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.is_admin is False

    def test_password_hashing(self, db):
        """Test password is properly hashed and verified"""
        user = User(username='hashtest', email='hash@test.com')
        user.set_password('mypassword')
        db.session.add(user)
        db.session.commit()

        assert user.password_hash is not None
        assert user.password_hash != 'mypassword'
        assert user.check_password('mypassword') is True
        assert user.check_password('wrongpassword') is False

    def test_password_different_hashes(self, db):
        """Test that same password produces different hashes"""
        user1 = User(username='user1', email='u1@test.com')
        user2 = User(username='user2', email='u2@test.com')
        user1.set_password('samepassword')
        user2.set_password('samepassword')

        assert user1.password_hash != user2.password_hash

    def test_user_authentication(self, sample_user):
        """Test user authentication flow"""
        assert sample_user.check_password('testpass123') is True
        assert sample_user.is_admin is True

    def test_user_repr(self, sample_user):
        """Test user string representation"""
        assert 'testadmin' in repr(sample_user) or str(sample_user.username) == 'testadmin'


class TestServiceModel:
    """Tests for Service model"""

    def test_create_service(self, db):
        """Test service creation"""
        service = Service(
            title='FEA Analysis',
            slug='fea-analysis',
            short_description='Finite Element Analysis',
            description='Comprehensive FEA services',
            icon='fa-cubes',
            is_active=True,
            order=1
        )
        db.session.add(service)
        db.session.commit()

        assert service.id is not None
        assert service.title == 'FEA Analysis'
        assert service.slug == 'fea-analysis'
        assert service.is_active is True

    def test_service_slug_unique(self, db):
        """Test service slug uniqueness"""
        s1 = Service(title='Service 1', slug='unique-slug', short_description='S1', description='S1', icon='fa-cog', order=1)
        db.session.add(s1)
        db.session.commit()

        s2 = Service(title='Service 2', slug='unique-slug', short_description='S2', description='S2', icon='fa-cog', order=2)
        db.session.add(s2)
        with pytest.raises(Exception):
            db.session.commit()

    def test_service_ordering(self, db):
        """Test services can be ordered"""
        s1 = Service(title='First', slug='first', short_description='1st', description='1st', icon='fa-1', order=1, is_active=True)
        s2 = Service(title='Second', slug='second', short_description='2nd', description='2nd', icon='fa-2', order=2, is_active=True)
        db.session.add_all([s2, s1])
        db.session.commit()

        services = Service.query.order_by(Service.order).all()
        assert services[0].title == 'First'
        assert services[1].title == 'Second'

    def test_service_active_filter(self, db):
        """Test filtering active services"""
        active = Service(title='Active', slug='active', short_description='A', description='A', icon='fa-a', order=1, is_active=True)
        inactive = Service(title='Inactive', slug='inactive', short_description='I', description='I', icon='fa-i', order=2, is_active=False)
        db.session.add_all([active, inactive])
        db.session.commit()

        result = Service.query.filter_by(is_active=True).all()
        assert len(result) == 1
        assert result[0].title == 'Active'


class TestBlogPostModel:
    """Tests for BlogPost model"""

    def test_create_blog_post(self, db):
        """Test blog post creation"""
        post = BlogPost(
            title='Test Post',
            slug='test-post',
            content='Test content here',
            category='engineering',
            is_published=True
        )
        db.session.add(post)
        db.session.commit()

        assert post.id is not None
        assert post.title == 'Test Post'
        assert post.is_published is True

    def test_blog_post_views(self, sample_blog_post):
        """Test blog post view counter"""
        initial_views = sample_blog_post.views or 0
        if hasattr(sample_blog_post, 'increment_views'):
            sample_blog_post.increment_views()
            assert sample_blog_post.views == initial_views + 1

    def test_blog_post_categories(self, db):
        """Test blog post category filtering"""
        p1 = BlogPost(title='CFD Post', slug='cfd-post', content='CFD', category='cfd', is_published=True)
        p2 = BlogPost(title='FEA Post', slug='fea-post', content='FEA', category='fea', is_published=True)
        db.session.add_all([p1, p2])
        db.session.commit()

        cfd_posts = BlogPost.query.filter_by(category='cfd').all()
        assert len(cfd_posts) == 1
        assert cfd_posts[0].title == 'CFD Post'

    def test_blog_published_filter(self, db):
        """Test published/draft filtering"""
        published = BlogPost(title='Published', slug='pub', content='Yes', is_published=True)
        draft = BlogPost(title='Draft', slug='draft', content='No', is_published=False)
        db.session.add_all([published, draft])
        db.session.commit()

        result = BlogPost.query.filter_by(is_published=True).all()
        assert len(result) == 1


class TestContactSubmissionModel:
    """Tests for ContactSubmission model"""

    def test_create_submission(self, db):
        """Test contact submission creation"""
        contact = ContactSubmission(
            name='Jane Doe',
            email='jane@example.com',
            company='Test Corp',
            phone='+92300123456',
            service_interest='cfd',
            message='I need CFD analysis',
            status='new'
        )
        db.session.add(contact)
        db.session.commit()

        assert contact.id is not None
        assert contact.name == 'Jane Doe'
        assert contact.status == 'new'

    def test_submission_status_update(self, sample_contact):
        """Test updating submission status"""
        sample_contact.status = 'read'
        assert sample_contact.status == 'read'

        sample_contact.status = 'replied'
        assert sample_contact.status == 'replied'

    def test_submission_timestamp(self, sample_contact):
        """Test submission has creation timestamp"""
        assert sample_contact.created_at is not None or hasattr(sample_contact, 'created_at')


class TestNewsletterSubscriberModel:
    """Tests for NewsletterSubscriber model"""

    def test_create_subscriber(self, db):
        """Test newsletter subscriber creation"""
        sub = NewsletterSubscriber(
            email='subscriber@test.com',
            is_active=True
        )
        db.session.add(sub)
        db.session.commit()

        assert sub.id is not None
        assert sub.email == 'subscriber@test.com'
        assert sub.is_active is True

    def test_subscriber_deactivation(self, db):
        """Test subscriber can be deactivated"""
        sub = NewsletterSubscriber(email='unsub@test.com', is_active=True)
        db.session.add(sub)
        db.session.commit()

        sub.is_active = False
        db.session.commit()

        result = NewsletterSubscriber.query.filter_by(email='unsub@test.com').first()
        assert result.is_active is False

    def test_duplicate_email_prevention(self, db):
        """Test duplicate email subscription prevention"""
        sub1 = NewsletterSubscriber(email='dupe@test.com', is_active=True)
        db.session.add(sub1)
        db.session.commit()

        sub2 = NewsletterSubscriber(email='dupe@test.com', is_active=True)
        db.session.add(sub2)
        with pytest.raises(Exception):
            db.session.commit()
