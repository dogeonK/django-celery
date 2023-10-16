import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj',
            broker='amqp://',
            backend='rpc://',
            include=['proj.tasks'])

app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')