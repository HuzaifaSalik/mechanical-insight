"""Newsletter subscription handlers"""
from flask import request, jsonify, flash, redirect, url_for
from app.main import main_bp
from app.models import NewsletterSubscriber, db
from datetime import datetime
import re


def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@main_bp.route('/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    """Handle newsletter subscription"""
    email = request.form.get('email', '').strip().lower()

    # Validate email
    if not email or not is_valid_email(email):
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400
        flash('Please enter a valid email address.', 'danger')
        return redirect(request.referrer or url_for('main.index'))

    # Check for duplicate subscription
    existing = NewsletterSubscriber.query.filter_by(email=email).first()
    if existing:
        if existing.is_active:
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'This email is already subscribed.'}), 409
            flash('This email is already subscribed to our newsletter.', 'info')
            return redirect(request.referrer or url_for('main.index'))
        else:
            # Reactivate subscription
            existing.is_active = True
            existing.subscribed_at = datetime.utcnow()
            db.session.commit()

            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': True, 'message': 'Welcome back! Your subscription has been reactivated.'})
            flash('Welcome back! Your subscription has been reactivated.', 'success')
            return redirect(request.referrer or url_for('main.index'))

    # Create new subscription
    subscriber = NewsletterSubscriber(
        email=email,
        is_active=True,
        subscribed_at=datetime.utcnow(),
        ip_address=request.remote_addr
    )

    try:
        db.session.add(subscriber)
        db.session.commit()

        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Thank you for subscribing to our newsletter!'})
        flash('Thank you for subscribing to our newsletter!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error saving newsletter subscription: {e}")

        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'An error occurred. Please try again.'}), 500
        flash('An error occurred. Please try again.', 'danger')

    return redirect(request.referrer or url_for('main.index'))


@main_bp.route('/newsletter/unsubscribe', methods=['POST'])
def newsletter_unsubscribe():
    """Handle newsletter unsubscription"""
    email = request.form.get('email', '').strip().lower()

    subscriber = NewsletterSubscriber.query.filter_by(email=email).first()
    if subscriber:
        subscriber.is_active = False
        db.session.commit()

    flash('You have been unsubscribed from our newsletter.', 'info')
    return redirect(url_for('main.index'))
