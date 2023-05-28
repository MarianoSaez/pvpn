from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class PrivateNetworkParameters(FlaskForm):
    ssid = StringField('SSID', validators=[DataRequired()])
    key = PasswordField('New password', validators=[])

class PublicNetworkParameters(FlaskForm):
    pass

class VpnParameters(FlaskForm):
    file = FileField("OpenVPN configuration file")
    username = StringField('username', validators=[])
    password = PasswordField('password', validators=[])
