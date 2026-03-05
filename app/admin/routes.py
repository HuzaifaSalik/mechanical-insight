from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.admin import admin_bp
from app.models import User, ContactSubmission, db
from werkzeug.security import generate_password_hash


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_panel.dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('admin/login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    """Logout admin user"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    # Get recent contact submissions
    recent_submissions = ContactSubmission.query.order_by(
        ContactSubmission.created_at.desc()
    ).limit(10).all()

    # Get statistics
    stats = {
        'total_submissions': ContactSubmission.query.count(),
        'new_submissions': ContactSubmission.query.filter_by(status='new').count(),
    }

    return render_template('admin/dashboard.html',
                         recent_submissions=recent_submissions,
                         stats=stats)


@admin_bp.route('/contacts')
@login_required
def contacts():
    """View all contact submissions"""
    page = request.args.get('page', 1, type=int)
    submissions = ContactSubmission.query.order_by(
        ContactSubmission.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)

    return render_template('admin/contacts.html', submissions=submissions)
