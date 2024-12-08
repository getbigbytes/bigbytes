from bigbytes.data_preparation.repo_manager import get_repo_config
from bigbytes.orchestration.queue.config import QueueConfig, QueueType


class QueueFactory:
    queue = None

    @classmethod
    def get_queue(self):
        if self.queue is not None:
            return self.queue

        queue_config = QueueConfig.load(config=get_repo_config().queue_config or dict())
        if queue_config.queue_type == QueueType.CELERY:
            from bigbytes.orchestration.queue.celery_queue import CeleryQueue
            self.queue = CeleryQueue(queue_config)
        else:
            from bigbytes.orchestration.queue.process_queue import ProcessQueue
            self.queue = ProcessQueue(queue_config)
        return self.queue
