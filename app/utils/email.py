from flask_mail import Message
from flask import current_app


def send_contact_notification(mail, submission):
    """Send email notification to admin about new contact submission"""
    try:
        msg = Message(
            subject=f'New Contact Form Submission from {submission.name}',
            recipients=[current_app.config.get('ADMIN_EMAIL', 'admin@companyinsight.com')],
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
        return True
    except Exception as e:
        print(f"Error sending admin notification: {e}")
        return False


def send_contact_confirmation(mail, submission):
    """Send confirmation email to user after form submission"""
    try:
        msg = Message(
            subject='Thank you for contacting Company Insight',
            recipients=[submission.email],
            body=f"""
Dear {submission.name},

Thank you for contacting Company Insight. We have received your message and will get back to you as soon as possible.

Your Message:
{submission.message}

If you have any urgent inquiries, please don't hesitate to reach out to us directly.

Best regards,
Company Insight Team
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending confirmation email: {e}")
        return False


def send_newsletter_welcome(mail, email):
    """Send welcome email to new newsletter subscriber"""
    try:
        msg = Message(
            subject='Welcome to Company Insight Newsletter',
            recipients=[email],
            body=f"""
Thank you for subscribing to the Company Insight newsletter!

You'll receive updates on:
- Latest engineering projects and case studies
- Industry insights and technical articles
- New service offerings and company news

Best regards,
Company Insight Team
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending newsletter welcome: {e}")
        return False
