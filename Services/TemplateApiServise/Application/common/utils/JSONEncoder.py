import json
from uuid import UUID


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        return super().default(o)
