import os
from celery import Celery
from circus.client import CircusClient

celery = Celery('tasks', broker=os.environ.get(
        'CELERY_BROKER_URI', 'redis://localhost:6379/0'))


@celery.task(name='tasks.create-watcher')
def create_watcher(sid=None):
    client = CircusClient()
    client.send_message(
        'add',
        cmd="scrapy runspider searchology/crawl/spidology.py -a {}".format(sid),
        name="spidology",
        autostart=True,
        respawn=False,
        working_dir='/vagrant/'
    )
