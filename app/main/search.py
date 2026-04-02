"""Global search functionality across blog and portfolio"""
from flask import render_template, request
from app.main import main_bp
from app.models import BlogPost, CaseStudy, Service
from sqlalchemy import or_


@main_bp.route('/search')
def search():
    """Global search across blog posts, portfolio, and services"""
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10

    results = {
        'blog_posts': [],
        'case_studies': [],
        'services': [],
        'total': 0
    }

    if query and len(query) >= 2:
        # Search blog posts
        blog_results = BlogPost.query.filter(
            BlogPost.is_published == True,
            or_(
                BlogPost.title.ilike(f'%{query}%'),
                BlogPost.subtitle.ilike(f'%{query}%'),
                BlogPost.content.ilike(f'%{query}%'),
                BlogPost.tags.ilike(f'%{query}%')
            )
        ).order_by(BlogPost.published_at.desc()).limit(10).all()

        # Search case studies
        case_results = CaseStudy.query.filter(
            CaseStudy.is_published == True,
            or_(
                CaseStudy.title.ilike(f'%{query}%'),
                CaseStudy.description.ilike(f'%{query}%'),
                CaseStudy.challenge.ilike(f'%{query}%'),
                CaseStudy.solution.ilike(f'%{query}%'),
                CaseStudy.technologies.ilike(f'%{query}%'),
                CaseStudy.industry.ilike(f'%{query}%')
            )
        ).order_by(CaseStudy.created_at.desc()).limit(10).all()

        # Search services
        service_results = Service.query.filter(
            Service.is_active == True,
            or_(
                Service.title.ilike(f'%{query}%'),
                Service.description.ilike(f'%{query}%'),
                Service.short_description.ilike(f'%{query}%')
            )
        ).order_by(Service.order).all()

        results['blog_posts'] = blog_results
        results['case_studies'] = case_results
        results['services'] = service_results
        results['total'] = len(blog_results) + len(case_results) + len(service_results)

    return render_template('main/search_results.html',
                         query=query,
                         results=results)
