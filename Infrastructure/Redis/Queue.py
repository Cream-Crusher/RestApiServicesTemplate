from redis import Redis
from rq import Queue

from config import config

task_queue = Queue(connection=Redis(config.redis_config.host))
