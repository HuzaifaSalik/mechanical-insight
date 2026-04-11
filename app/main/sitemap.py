"""Sitemap generation for SEO"""
from flask import make_response, render_template_string
from app.main import main_bp
from app.models import Service, BlogPost, CaseStudy
from app.utils.seo import generate_sitemap_entries


SITEMAP_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{% for entry in entries %}
    <url>
        <loc>{{ entry.loc }}</loc>
        <lastmod>{{ entry.lastmod }}</lastmod>
        <changefreq>{{ entry.changefreq }}</changefreq>
        <priority>{{ entry.priority }}</priority>
    </url>
{% endfor %}
</urlset>"""


@main_bp.route('/sitemap.xml')
def sitemap():
    """Generate XML sitemap for search engines"""
    services = Service.query.filter_by(is_active=True).all()
    blog_posts = BlogPost.query.filter_by(is_published=True).all()
    case_studies = CaseStudy.query.filter_by(is_published=True).all()
    
    entries = generate_sitemap_entries(services, blog_posts, case_studies)
    
    sitemap_xml = render_template_string(SITEMAP_TEMPLATE, entries=entries)
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response


@main_bp.route('/robots.txt')
def robots():
    """Serve robots.txt"""
    return main_bp.send_static_file('robots.txt')
