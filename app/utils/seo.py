"""SEO optimization utilities"""
from flask import request, url_for
from datetime import datetime


def generate_meta_tags(title=None, description=None, keywords=None, image=None, page_type='website'):
    """Generate meta tags for a page"""
    site_name = 'Mechanical Insight - Engineering Services'
    default_description = 'Professional mechanical engineering services including CAD modeling, FEA analysis, CFD simulations, and thermal analysis.'
    default_keywords = 'mechanical engineering, CAD modeling, FEA analysis, CFD simulation, thermal analysis, product design, aerospace engineering, automotive engineering'
    
    meta = {
        'title': f'{title} | {site_name}' if title else site_name,
        'description': description or default_description,
        'keywords': keywords or default_keywords,
        'og_title': title or site_name,
        'og_description': description or default_description,
        'og_type': page_type,
        'og_url': request.url,
        'og_site_name': site_name,
        'og_image': image or url_for('static', filename='images/og-default.jpg', _external=True),
        'twitter_card': 'summary_large_image',
        'twitter_title': title or site_name,
        'twitter_description': description or default_description,
        'canonical_url': request.url,
    }
    return meta


def generate_breadcrumbs(items):
    """Generate structured data breadcrumbs for SEO"""
    breadcrumbs = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': []
    }
    for i, item in enumerate(items, 1):
        breadcrumbs['itemListElement'].append({
            '@type': 'ListItem',
            'position': i,
            'name': item['name'],
            'item': item.get('url', '')
        })
    return breadcrumbs


def generate_organization_schema():
    """Generate Organization structured data"""
    return {
        '@context': 'https://schema.org',
        '@type': 'Organization',
        'name': 'Mechanical Insight',
        'description': 'Professional mechanical engineering services company',
        'url': 'https://mechanical-insight.onrender.com',
        'logo': 'https://mechanical-insight.onrender.com/static/images/logo.png',
        'contactPoint': {
            '@type': 'ContactPoint',
            'contactType': 'customer service',
            'availableLanguage': 'English'
        },
        'sameAs': []
    }


def generate_service_schema(service):
    """Generate Service structured data for individual service pages"""
    return {
        '@context': 'https://schema.org',
        '@type': 'Service',
        'name': service.title,
        'description': service.short_description,
        'provider': {
            '@type': 'Organization',
            'name': 'Mechanical Insight'
        },
        'serviceType': 'Engineering Services',
        'areaServed': 'Worldwide'
    }


def generate_article_schema(post):
    """Generate Article structured data for blog posts"""
    return {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': post.title,
        'description': post.subtitle if hasattr(post, 'subtitle') else '',
        'datePublished': post.published_at.isoformat() if post.published_at else '',
        'dateModified': post.updated_at.isoformat() if hasattr(post, 'updated_at') and post.updated_at else '',
        'author': {
            '@type': 'Organization',
            'name': 'Mechanical Insight'
        },
        'publisher': {
            '@type': 'Organization',
            'name': 'Mechanical Insight'
        }
    }


def generate_sitemap_entries(services, blog_posts, case_studies):
    """Generate sitemap XML entries"""
    entries = []
    base_url = 'https://mechanical-insight.onrender.com'
    now = datetime.utcnow().strftime('%Y-%m-%d')
    
    # Static pages
    static_pages = [
        ('/', '1.0', 'weekly'),
        ('/about', '0.8', 'monthly'),
        ('/services', '0.9', 'weekly'),
        ('/contact', '0.7', 'monthly'),
        ('/blog/', '0.8', 'daily'),
        ('/portfolio/', '0.8', 'weekly'),
    ]
    
    for url, priority, freq in static_pages:
        entries.append({
            'loc': f'{base_url}{url}',
            'lastmod': now,
            'changefreq': freq,
            'priority': priority
        })
    
    # Service pages
    for service in services:
        entries.append({
            'loc': f'{base_url}/services/{service.slug}',
            'lastmod': now,
            'changefreq': 'monthly',
            'priority': '0.8'
        })
    
    # Blog posts
    for post in blog_posts:
        entries.append({
            'loc': f'{base_url}/blog/{post.slug}',
            'lastmod': post.published_at.strftime('%Y-%m-%d') if post.published_at else now,
            'changefreq': 'monthly',
            'priority': '0.6'
        })
    
    # Case studies
    for case in case_studies:
        entries.append({
            'loc': f'{base_url}/portfolio/{case.slug}',
            'lastmod': now,
            'changefreq': 'monthly',
            'priority': '0.7'
        })
    
    return entries
