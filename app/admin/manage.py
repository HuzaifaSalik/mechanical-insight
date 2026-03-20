"""Admin content management utilities"""
from app.models import ContactSubmission, BlogPost, CaseStudy, NewsletterSubscriber, Service, db


def get_dashboard_stats():
    """Get statistics for admin dashboard"""
    return {
        'total_contacts': ContactSubmission.query.count(),
        'new_contacts': ContactSubmission.query.filter_by(status='new').count(),
        'total_posts': BlogPost.query.count(),
        'published_posts': BlogPost.query.filter_by(is_published=True).count(),
        'total_cases': CaseStudy.query.count(),
        'total_subscribers': NewsletterSubscriber.query.filter_by(is_active=True).count(),
        'total_services': Service.query.filter_by(is_active=True).count(),
    }


def update_contact_status(submission_id, new_status):
    """Update contact submission status"""
    submission = ContactSubmission.query.get_or_404(submission_id)
    submission.status = new_status
    db.session.commit()
    return submission


def get_recent_submissions(limit=10):
    """Get recent contact submissions"""
    return ContactSubmission.query.order_by(
        ContactSubmission.created_at.desc()
    ).limit(limit).all()


def get_subscriber_list():
    """Get all active newsletter subscribers"""
    return NewsletterSubscriber.query.filter_by(
        is_active=True
    ).order_by(NewsletterSubscriber.subscribed_at.desc()).all()
