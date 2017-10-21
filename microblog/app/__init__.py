from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import config

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler

    credentials = (config.MAIL_USERNAME, config.MAIL_PASSWORD)
    mail_handler = SMTPHandler((config.MAIL_SERVER, config.MAIL_PORT),
                               'no-reply@' + config.MAIL_SERVER,
                               config.ADMINS,
                               'microblog failure',
                               credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

from app import views, models
