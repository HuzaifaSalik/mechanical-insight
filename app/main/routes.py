from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_mail import Message
from app.main import main_bp
from app.models import Service, CaseStudy, BlogPost, ContactSubmission, db
from app.main.forms import ContactForm
from app import mail, limiter
from datetime import datetime


@main_bp.route('/')
def index():
    """Homepage"""
    # Get featured case studies
    featured_cases = CaseStudy.query.filter_by(
        is_published=True, featured=True
    ).order_by(CaseStudy.order).limit(4).all()

    # Get all active services
    services = Service.query.filter_by(is_active=True).order_by(Service.order).all()

    # Get recent blog posts
    recent_posts = BlogPost.query.filter_by(
        is_published=True
    ).order_by(BlogPost.published_at.desc()).limit(3).all()

    return render_template('main/index.html',
                         featured_cases=featured_cases,
                         services=services,
                         recent_posts=recent_posts)


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')


@main_bp.route('/services')
def services():
    """Services overview page"""
    services = Service.query.filter_by(is_active=True).order_by(Service.order).all()
    return render_template('main/services.html', services=services)


@main_bp.route('/services/<slug>')
def service_detail(slug):
    """Individual service detail page"""
    service = Service.query.filter_by(slug=slug, is_active=True).first_or_404()

    # Get related case studies
    related_cases = CaseStudy.query.filter_by(
        service_id=service.id,
        is_published=True
    ).order_by(CaseStudy.order).limit(3).all()

    return render_template('main/service_detail.html',
                         service=service,
                         related_cases=related_cases)


@main_bp.route('/contact', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def contact():
    """Contact page with form submission"""
    form = ContactForm()

    if form.validate_on_submit():
        # Create contact submission
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
            # Save to database
            db.session.add(submission)
            db.session.commit()

            # Send email notification to admin
            send_contact_notification(submission)

            # Send confirmation email to user
            send_contact_confirmation(submission)

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


def send_contact_notification(submission):
    """Send email notification to admin about new contact submission"""
    try:
        msg = Message(
            subject=f'New Contact Form Submission from {submission.name}',
            recipients=[mail.app.config['ADMIN_EMAIL']],
            body=f"""
New contact form submission received:

Name: {submission.name}
Email: {submission.email}
Company: {submission.company or 'N/A'}
Phone: {submission.phone or 'N/A'}
Service Interest: {submission.service_interest or 'N/A'}

Message:
{submission.message}

Submitted at: {submission.created_at.strftime('%Y-%m-%d %H:%M:%S')}
IP Address: {submission.ip_address}
            """
        )
        mail.send(msg)
    except Exception as e:
        print(f"Error sending admin notification: {e}")


def send_contact_confirmation(submission):
    """Send confirmation email to user"""
    try:
        msg = Message(
            subject='Thank you for contacting Company Insight',
            recipients=[submission.email],
            body=f"""
Dear {submission.name},

Thank you for contacting Company Insight. We have received your message and will get back to you as soon as possible.

Your Message:
{submission.message}

Best regards,
Company Insight Team
            """
        )
        mail.send(msg)
    except Exception as e:
        print(f"Error sending confirmation email: {e}")
