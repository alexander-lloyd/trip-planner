from threading import Thread
from flask import current_app, render_template
from flask_mail import Message

from . import mail


def _send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, from_, subject, template, **kwargs):
    app = current_app._get_current_object()
    if not isinstance(to, list):
        to = list(to)
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=from_,
                  recipients=to)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    thr = Thread(target=_send_async_email, args=[app, msg])
    thr.start()
    return thr