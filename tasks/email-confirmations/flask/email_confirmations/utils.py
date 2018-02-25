from flask import render_template, url_for


def send_email_through_postmark(client, from_, to, subject, content):
    client.emails.send(
        From=from_,
        To=to,
        Subject=subject,
        HtmlBody=content
    )


def send_confirmation_email_through_postmark(client, user, from_):
    send_email_through_postmark(
        client,
        from_=from_,
        to=user.email,
        subject='Confirm your email',
        content=render_template(
            'activation_email.html',
            user=user,
            confirmation_url=url_for('confirm', user_id=user.id, _external=True)))
