import os
from celery import Celery
from circus.client import CircusClient

celery = Celery('tasks', broker=os.environ.get(
        'CELERY_BROKER_URI', 'redis://localhost:6379/0'))

client = CircusClient()

msg = '{"command": "add","properties":{"cmd": "/vagrant/env/bin/scrapy runspider crawl/spidology.py","name":"spidology"}}'

def _send_cmd():
    client.send_message('status')
    # client.send_message('add', cmd="/vagrant/env/bin/scrapy runspider crawl/spidology.py", name="spidology")

@celery.task(name='tasks.create-watcher')
def create_watcher():
    _send_cmd()

@celery.task(name='tasks.foo')
def bar():
    print 'hello'
