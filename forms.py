from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import (DataRequired, Length, Email, EqualTo,
                                ValidationError)
from models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                     EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        # Check if user exists
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another.')

    def validate_email(self, email):
        # Check if user exists
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # Remembers user for a certain period after closing their browser
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')
