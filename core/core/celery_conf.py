import datetime
from time import sleep
from celery import Celery
from core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL,
)


celery_app.conf.update(
    broker_connection_retry_on_startup=True,  # Add this line to avoid the warning
    timezone="UTC",
    beat_schedule={ 
    "print hello-every-minute": {
    "task": "core.celery_conf.print_hello",
    "schedule": 30,  # every minute
    },
    },
)

@celery_app.task
def sum_number(x,y):
    sleep(10)
    return x*y


@celery_app.task
def print_hello():
    now = datetime.datetime.now().strftime("%Y-%m-%d %N:%M:%S")
    print(f"Hello! Current time: (now)")