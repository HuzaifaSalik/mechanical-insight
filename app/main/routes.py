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


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form submission and validation"""
    from app.main.forms import ContactForm
    form = ContactForm()

    if form.validate_on_submit():
        # Create contact submission record
        submission = ContactSubmission(
            name=form.name.data,
            email=form.email.data,
            company=form.company.data,
            phone=form.phone.data,
            service_interest=form.service_interest.data,
            message=form.message.data,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            status='new'
        )

        try:
            db.session.add(submission)
            db.session.commit()

            # Handle AJAX requests
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': 'Thank you for contacting us! We will get back to you soon.'
                })

            flash('Thank you for contacting us! We will get back to you soon.', 'success')
            return redirect(url_for('main.contact'))

        except Exception as e:
            db.session.rollback()
            print(f"Error saving contact submission: {e}")

            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'message': 'An error occurred. Please try again later.'
                }), 500

            flash('An error occurred. Please try again later.', 'danger')

    return render_template('main/contact.html', form=form)
