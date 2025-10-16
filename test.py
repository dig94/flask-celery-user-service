import time
from celery import group
from tasks.user_tasks import send_welcome_email

emails = [f"user{i}@example.com" for i in range(12)]
job = group(send_welcome_email.s(e) for e in emails)

t0 = time.time()
res = job.apply_async()
res.get()  # wait for all to finish
print("Total wall time:", round(time.time() - t0, 2), "sec")
