from flask_wtf import FlaskForm as BaseForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length

from app.models import User


class LoginForm(BaseForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class EditForm(BaseForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        BaseForm.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not BaseForm.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append('This nickname is already in use.')
            return False
        return True
