from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField,SubmitField,FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    organization = StringField('Organization', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class DataForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    market = StringField('Market', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    commodity = StringField('Commodity', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])
    currency = StringField('Currency', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UploadForm(FlaskForm):
    data = FileField('Choose CSV file', validators=[FileRequired(), FileAllowed(['csv'])])
    submit = SubmitField('Upload')
