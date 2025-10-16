from celery_app import celery
import time

@celery.task
def send_welcome_email(user_email):
    print("Celery broker URL:", celery.conf.broker_url)
    # simulate sending email
    time.sleep(5)
    return f"Welcome email sent to {user_email}"
