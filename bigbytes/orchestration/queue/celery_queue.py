from typing import Callable

from bigbytes.orchestration.queue.config import QueueConfig
from bigbytes.orchestration.queue.queue import Queue


class CeleryQueue(Queue):
    """
    TODO: implement this class.
    """

    def __init__(self, queue_config: QueueConfig):
        # self.celery_app = Celery(
        #     'mypackage',
        #     broker='amqp://guest@localhost//',
        #     backend='amqp://guest@localhost//',
        # )
        pass

    def clean_up_jobs(self):
        pass

    def enqueue(self, job_id: str, target: Callable, *args, **kwargs):
        pass

    def has_job(self, job_id: str):
        return False

    def kill_job(self, job_id: str):
        pass

    def start(self):
        pass

    def stop(self):
        pass
