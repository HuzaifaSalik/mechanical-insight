from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional


class ContactForm(FlaskForm):
    """Contact form with validation"""
    name = StringField('Full Name',
                      validators=[DataRequired(), Length(min=2, max=100)])

    email = StringField('Email Address',
                       validators=[DataRequired(), Email()])

    company = StringField('Company Name',
                         validators=[Optional(), Length(max=200)])

    phone = StringField('Phone Number',
                       validators=[Optional(), Length(max=20)])

    service_interest = SelectField('Service Interest',
                                  choices=[
                                      ('', 'Select a Service'),
                                      ('product-design-cad', 'Product Design & CAD Modeling'),
                                      ('mechanical-fea', 'Mechanical Design & Structural Analysis (FEA)'),
                                      ('automotive', 'Automotive & Transportation Simulations'),
                                      ('aerospace', 'Aerospace & UAV Engineering Support'),
                                      ('manufacturing', 'Manufacturing & Industrial Equipment Analysis'),
                                      ('cfd', 'CFD Simulations'),
                                      ('thermal', 'Thermal & Heat Transfer Analysis'),
                                      ('other', 'Other')
                                  ])

    message = TextAreaField('Message',
                           validators=[DataRequired(), Length(min=10, max=2000)])

    newsletter = BooleanField('Subscribe to newsletter')

    # Uncomment when reCAPTCHA keys are configured
    # recaptcha = RecaptchaField()

    submit = SubmitField('Send Message')
