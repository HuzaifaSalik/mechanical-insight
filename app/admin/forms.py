from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Admin login form"""
    username = StringField('Username',
                          validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password',
                            validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')
