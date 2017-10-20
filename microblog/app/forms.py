from flask_wtf import FlaskForm as BaseForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(BaseForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
