from django.core.mail import send_mail
from celery_tasks1.main import app


@app.task
def send_mail_celery(subject, message, from_email, recipient_list, html_message):
    send_mail(
        subject = subject,
        message = message,
        from_email = from_email,
        recipient_list = recipient_list,
        html_message = html_message
    )



