from flask_mail import Message
from app.extensions import mail
from celery_runner import celery


@celery.task(bind=True, time_limit=60, rate_limit='20/m', max_retries=10, default_retry_delay=30,
             ignore_result=True)
def send_email(self, data):
    try:
        msg = Message(subject="Contact Us Feedback", recipients=['cybera.3s@gmail.com'])

        msg.html = f"""<h1>From: {data['email']}</h1>
            <h1>First Name: {data['first_name']}</h1>
            <h1>Last Name: {data['last_name']}</h1>
            </h1><p>Feedback: {data['feedback']}</p>"""

        mail.send(msg)
        return "Email Sent"
    except Exception as e:
        self.retry(exc=e)