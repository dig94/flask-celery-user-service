# celery_app.py
from celery import Celery
import os
from dotenv import load_dotenv
load_dotenv()
celery = Celery(
    "my_app",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
    include=["tasks.user_tasks"]
)
