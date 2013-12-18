import os
from celery import Celery
from circus.client import CircusClient
# from circus.stream.file_stream import FileStream

celery = Celery('tasks', broker=os.environ.get(
        'CELERY_BROKER_URI', 'redis://localhost:6379/0'))

spidology_path = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)
    ), os.pardir, 'crawl', 'spidology.py')


@celery.task(name='tasks.create-watcher')
def create_watcher():
    print 'here'
    os.environ['JAVA_HOME'] = '/usr/lib/jvm/default-java'
    client = CircusClient()
    client.send_message(
        'add',
        # cmd="scrapy runspider {}".format(spidology_path),
        cmd="/vagrant/env/bin/scrapy runspider /vagrant/searchology/crawl/spidology.py",
        name="spidology",
        options={
            "respawn": False,
            "uid": "spidology",
            "gid": "spidology",
            "stdout_stream": {
                'class': 'FileStream',
                'filename': '/var/log/spidology_stdout.log',
                'refresh_time': 0.3
            },
            "stderr_stream": {
                'class': 'FileStream',
                'filename': '/var/log/spidology_stderr.log',
                'refresh_time': 0.3
            }
        },
        start=True,
    )

create_watcher()
