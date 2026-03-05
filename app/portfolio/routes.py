from flask import render_template, request, abort
from app.portfolio import portfolio_bp
from app.models import CaseStudy, Service


@portfolio_bp.route('/')
def portfolio_list():
    """Portfolio/case studies listing page"""
    page = request.args.get('page', 1, type=int)
    per_page = 12

    # Filter by service
    service_filter = request.args.get('service', '')
    industry_filter = request.args.get('industry', '')

    # Build query
    query = CaseStudy.query.filter_by(is_published=True)

    if service_filter:
        query = query.filter_by(service_id=service_filter)

    if industry_filter:
        query = query.filter_by(industry=industry_filter)

    # Get paginated results
    case_studies = query.order_by(CaseStudy.order, CaseStudy.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Get all services for filter
    services = Service.query.filter_by(is_active=True).order_by(Service.order).all()

    # Get all industries for filter
    industries = CaseStudy.query.with_entities(CaseStudy.industry).filter(
        CaseStudy.is_published == True,
        CaseStudy.industry.isnot(None)
    ).distinct().all()
    industries = [i[0] for i in industries if i[0]]

    return render_template('portfolio/portfolio_list.html',
                         case_studies=case_studies,
                         services=services,
                         industries=industries,
                         current_service=service_filter,
                         current_industry=industry_filter)


@portfolio_bp.route('/<slug>')
def case_study_detail(slug):
    """Individual case study detail page"""
    case_study = CaseStudy.query.filter_by(slug=slug, is_published=True).first_or_404()

    # Get related case studies (same service)
    related_cases = CaseStudy.query.filter(
        CaseStudy.id != case_study.id,
        CaseStudy.is_published == True,
        CaseStudy.service_id == case_study.service_id
    ).order_by(CaseStudy.order).limit(3).all()

    return render_template('portfolio/case_study.html',
                         case_study=case_study,
                         related_cases=related_cases)
