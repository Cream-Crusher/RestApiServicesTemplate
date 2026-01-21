from rq import Queue

from Services.TemplateApiServise.Persistence.Repository.Cache.CacheInstanceRepository import cache_repository_instance

task_queue = Queue("default", connection=cache_repository_instance)
