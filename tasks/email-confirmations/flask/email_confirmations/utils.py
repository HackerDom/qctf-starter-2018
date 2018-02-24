from flask import render_template, url_for
from flask_mail import Mail, Message


mail_manager = Mail()


def send_email(to, subject, content):
    msg = Message(
        subject,
        recipients=[to],
        html=content)
    mail_manager.send(msg)


def send_confirmation_email(user):
    send_email(
        to=user.email,
        subject='Confirm your email',
        content=render_template(
            'activation_email.html',
            user=user,
            confirmation_url=url_for('confirm', user_id=user.id, _external=True)))
