from Services.TemplateApiServise.Domain.BaseEntity import BaseEntity


class ModelNotFound(Exception):

    def __init__(self, model: type[BaseEntity]):
        self.message = f"Model {model.__tablename__} not found"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"
