"""Integration tests for all application routes"""
import pytest
from app.models import User, Service, BlogPost, CaseStudy, ContactSubmission


class TestPublicRoutes:
    """Tests for public-facing routes"""

    def test_homepage_returns_200(self, client):
        """Test homepage loads successfully"""
        response = client.get('/')
        assert response.status_code == 200

    def test_about_page(self, client):
        """Test about page loads"""
        response = client.get('/about')
        assert response.status_code == 200

    def test_services_page(self, client):
        """Test services listing page"""
        response = client.get('/services')
        assert response.status_code == 200

    def test_service_detail_valid(self, client, sample_service):
        """Test individual service page with valid slug"""
        response = client.get(f'/services/{sample_service.slug}')
        assert response.status_code == 200

    def test_service_detail_invalid_slug(self, client):
        """Test service page with invalid slug returns 404"""
        response = client.get('/services/nonexistent-service')
        assert response.status_code == 404

    def test_contact_page_get(self, client):
        """Test contact page loads with GET"""
        response = client.get('/contact')
        assert response.status_code == 200

    def test_search_page(self, client):
        """Test search page loads"""
        response = client.get('/search?q=test')
        assert response.status_code == 200

    def test_search_empty_query(self, client):
        """Test search with empty query"""
        response = client.get('/search?q=')
        assert response.status_code == 200

    def test_404_page(self, client):
        """Test 404 error page"""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404


class TestContactFormSubmission:
    """Tests for contact form submission"""

    def test_contact_form_valid_submission(self, client, db):
        """Test valid contact form submission"""
        response = client.post('/contact', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'company': 'Test Corp',
            'phone': '+923001234567',
            'service_interest': 'cfd',
            'message': 'I need CFD analysis services for my project',
            'csrf_token': 'test'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_contact_form_missing_required(self, client):
        """Test contact form with missing required fields"""
        response = client.post('/contact', data={
            'name': '',
            'email': '',
            'message': ''
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_contact_form_invalid_email(self, client):
        """Test contact form with invalid email"""
        response = client.post('/contact', data={
            'name': 'Test',
            'email': 'not-an-email',
            'message': 'Test message content here'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_contact_ajax_submission(self, client, db):
        """Test AJAX contact form submission"""
        response = client.post('/contact', 
            data={
                'name': 'Ajax User',
                'email': 'ajax@test.com',
                'message': 'Testing AJAX submission flow'
            },
            headers={'X-Requested-With': 'XMLHttpRequest'},
            follow_redirects=True
        )
        assert response.status_code in [200, 400]


class TestBlogRoutes:
    """Tests for blog routes"""

    def test_blog_listing(self, client):
        """Test blog listing page"""
        response = client.get('/blog/')
        assert response.status_code == 200

    def test_blog_post_detail(self, client, sample_blog_post):
        """Test individual blog post page"""
        response = client.get(f'/blog/{sample_blog_post.slug}')
        assert response.status_code == 200

    def test_blog_invalid_slug(self, client):
        """Test blog with invalid slug"""
        response = client.get('/blog/nonexistent-post')
        assert response.status_code == 404

    def test_blog_search(self, client):
        """Test blog search functionality"""
        response = client.get('/blog/?q=test')
        assert response.status_code == 200

    def test_blog_category_filter(self, client, sample_blog_post):
        """Test blog category filtering"""
        response = client.get(f'/blog/category/{sample_blog_post.category}')
        assert response.status_code == 200

    def test_blog_pagination(self, client):
        """Test blog pagination"""
        response = client.get('/blog/?page=1')
        assert response.status_code == 200


class TestPortfolioRoutes:
    """Tests for portfolio routes"""

    def test_portfolio_listing(self, client):
        """Test portfolio listing page"""
        response = client.get('/portfolio/')
        assert response.status_code == 200

    def test_portfolio_invalid_slug(self, client):
        """Test portfolio with invalid slug"""
        response = client.get('/portfolio/nonexistent-case')
        assert response.status_code == 404

    def test_portfolio_service_filter(self, client):
        """Test portfolio service filter"""
        response = client.get('/portfolio/?service=1')
        assert response.status_code == 200

    def test_portfolio_industry_filter(self, client):
        """Test portfolio industry filter"""
        response = client.get('/portfolio/?industry=automotive')
        assert response.status_code == 200


class TestAdminAuthentication:
    """Tests for admin authentication flow"""

    def test_admin_login_page(self, client):
        """Test admin login page loads"""
        response = client.get('/admin/login')
        assert response.status_code == 200

    def test_admin_login_valid(self, client, sample_user):
        """Test admin login with valid credentials"""
        response = client.post('/admin/login', data={
            'username': 'testadmin',
            'password': 'testpass123'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_admin_login_invalid(self, client):
        """Test admin login with invalid credentials"""
        response = client.post('/admin/login', data={
            'username': 'wronguser',
            'password': 'wrongpass'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_admin_dashboard_requires_login(self, client):
        """Test dashboard redirects when not logged in"""
        response = client.get('/admin/dashboard')
        assert response.status_code in [302, 401, 403]

    def test_admin_contacts_requires_login(self, client):
        """Test contacts page requires authentication"""
        response = client.get('/admin/contacts')
        assert response.status_code in [302, 401, 403]

    def test_admin_logout(self, client, sample_user):
        """Test admin logout"""
        # Login first
        client.post('/admin/login', data={
            'username': 'testadmin',
            'password': 'testpass123'
        })
        # Then logout
        response = client.get('/admin/logout', follow_redirects=True)
        assert response.status_code == 200


class TestNewsletterRoutes:
    """Tests for newsletter subscription routes"""

    def test_newsletter_subscribe(self, client, db):
        """Test newsletter subscription"""
        response = client.post('/newsletter/subscribe', data={
            'email': 'newstest@example.com'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_newsletter_invalid_email(self, client):
        """Test newsletter with invalid email"""
        response = client.post('/newsletter/subscribe', 
            data={'email': 'invalid'},
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        assert response.status_code in [200, 400]

    def test_newsletter_empty_email(self, client):
        """Test newsletter with empty email"""
        response = client.post('/newsletter/subscribe',
            data={'email': ''},
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        assert response.status_code in [200, 400]
