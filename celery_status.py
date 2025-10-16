from celery_app import celery

result = celery.AsyncResult('afed0fbf-4461-434c-9414-10be13c4afab')
print(result.status)  # PENDING, STARTED, SUCCESS
print(result.result)  # "Welcome email sent to john@example.com"
