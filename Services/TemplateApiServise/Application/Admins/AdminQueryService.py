import uuid

from Services.TemplateApiServise.Application.common.BaseQueryService import BaseQueryService
from Services.TemplateApiServise.Domain.Admin import Admin


class AdminQueryService(BaseQueryService[Admin, uuid.UUID]):

    def __init__(self):
        super().__init__(model=Admin)


admin_query_service = AdminQueryService()
