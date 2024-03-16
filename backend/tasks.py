from __init__ import mail
from flask_mail import Message
from models import User
from flask import render_template
from celery import shared_task


def send_welcome(email):
    sender = 'noreply@app.com'
    subject = "Welcome to Trance!"
    msg = Message(subject=subject, sender=sender, recipients=[email])
    msg.body = ""
    username = User.query.filter_by(email=email).first().username
    data = {
        'app_name': "Trance",
        "title": f"Hey {username},",
    }
    msg.html = render_template('welcome.html', data=data)
    try:
        mail.send(msg)
        return {"message": f"Email sent successfully to {email}"}, 200
    except Exception as e:
        return (str(e))


def send_reminder(email):
    sender = 'noreply@app.com'
    subject = "🌟 Don't Miss Out on the Fun!"
    msg = Message(subject=subject, sender=sender, recipients=[email])
    msg.body = ""
    username = User.query.filter_by(email=email).first().username
    data = {
        'app_name': "Trance",
        "title": f"Hey {username},",
    }
    msg.html = render_template('reminder.html', data=data)
    try:
        mail.send(msg)
        return {"message": f"Email sent successfully to {email}"}, 200
    except Exception as e:
        return (str(e))


@shared_task(ignore_result=False)
def send_monthly_report(user):
    email = user.email
    if user:
        # Generate report data for the creator
        report_data = {
            'name': user.username,
            'total_songs': user.created_songs.count(),
            'total_albums': user.created_albums.count(),
            'total_likes': user.likes_received.count(),
            'total_reports': user.reports_received.count(),
            'total_streams': user.streams_received.count(),
            # Add more data if needed
        }

        # Render HTML content for the email using a template
        html_content = render_template(
            'email/monthly_report.html', data=report_data)

        # Create a Flask-Mail Message instance
        msg = Message(subject='Monthly Trance Creator Report',
                      sender='noreply@app.com',
                      recipients=[email])
        msg.html = html_content

        try:
            # Send email to the creator
            mail.send(msg)
            return {"message": f"Email sent successfully to {email}"}, 200
        except Exception as e:
            return str(e), 500
    else:
        return {"message": "User not found or not a creator"}, 404


@shared_task(ignore_result=False)
def remainder(email):
    return send_reminder(email)
