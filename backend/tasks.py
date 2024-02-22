from __init__ import mail
from flask_mail import Message
from models import User
from flask import render_template
from celery import shared_task


def send_welcome(email):
    sender = 'noreply@app.com'
    subject = "🌟 Don't Miss Out on the Fun! Your App Awaits Your Glorious Presence! 🚀"
    msg = Message(subject=subject, sender=sender, recipients=[email])
    msg.body = ""
    username = User.query.filter_by(email=email).first().username
    data = {
        'app_name': "Trance",
        "title": f"Hey {username},",
    }
    msg.html = render_template('email.html', data=data)
    try:
        mail.send(msg)
        return {"message": f"Email sent successfully to {email}"}, 200
    except Exception as e:
        return (str(e))


@shared_task(ignore_result=False)
def remainder(email):
    print("Hi")
    return send_welcome(email)
