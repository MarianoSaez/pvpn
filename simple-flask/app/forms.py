from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class PrivateNetworkParameters(FlaskForm):
    ssid = StringField('SSID', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired()])
    vpn_config = FileField('Upload VPN config file', validators=[DataRequired()])
