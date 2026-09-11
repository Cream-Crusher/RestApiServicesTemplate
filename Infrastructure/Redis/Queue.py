from rq import Queue

from Infrastructure.Redis.Client import redis_client

task_queue = Queue(connection=redis_client)
