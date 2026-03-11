from flask import render_template, request, flash, redirect, url_for, jsonify
from app.main import main_bp
from app.models import Service, CaseStudy, BlogPost, ContactSubmission, db
from datetime import datetime


@main_bp.route('/')
def index():
    """Homepage"""
    services = Service.query.filter_by(is_active=True).order_by(Service.order).all()
    return render_template('main/index.html', services=services)


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')


@main_bp.route('/services')
def services():
    """Services listing page - displays all 7 engineering services"""
    services = Service.query.filter_by(is_active=True).order_by(Service.order).all()
    return render_template('main/services.html', services=services)


@main_bp.route('/services/<slug>')
def service_detail(slug):
    """Individual service detail page with dynamic routing"""
    service = Service.query.filter_by(slug=slug, is_active=True).first_or_404()

    # Get related case studies for this service
    related_cases = CaseStudy.query.filter_by(
        service_id=service.id,
        is_published=True
    ).order_by(CaseStudy.order).limit(3).all()

    # Get other services for "Related Services" section
    other_services = Service.query.filter(
        Service.id != service.id,
        Service.is_active == True
    ).order_by(Service.order).limit(3).all()

    return render_template('main/service_detail.html',
                         service=service,
                         related_cases=related_cases,
                         other_services=other_services)
