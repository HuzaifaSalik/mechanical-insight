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
