import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from . import db
from .models import Request
from dotenv import load_dotenv
import os

load_dotenv()

def send_email(to_email, subject, body, cc_email=None):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    print(f" email: {sender_email}")
    print(f" pass: {sender_password}")
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    if cc_email:
        msg['Cc'] = cc_email

    # Combine the primary recipient and cc for delivery
    recipients = [to_email]
    if cc_email:
        recipients.append(cc_email)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")


def check_expirations_and_notify():
    now = datetime.utcnow()
    requests = Request.query.filter(Request.status == 'Pending').all()

    for req in requests:
        days_left = (req.expiration_date - now).days

        if days_left < 0:
            req.status = 'Expired'
            db.session.commit()
        elif days_left == 0:  # Expiration day
            send_email(
                to_email=req.receiver.email,
                subject="Request Expired",
                body=f"Hello {req.receiver.user_name},\n\nThe request from {req.name} has expired."
            )
        elif days_left == 5:  # 5 days before expiration
            send_email(
                to_email=req.receiver.email,
                subject="Request Expiration Reminder",
                body=f"Hello {req.receiver.user_name},\n\nThe request from {req.name} will expire in 5 days."
            )
