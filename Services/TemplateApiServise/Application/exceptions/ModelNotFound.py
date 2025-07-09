from Services.TemplateApiServise.Domain.BaseEntity import BaseEntity


class ModelNotFound(Exception):

    def __init__(self, model: type[BaseEntity], message: str = "Model {model_name} not found"):
        self.message = message.format(model_name=model.__tablename__)
        super().__init__(self.message)

    def __str__(self):
        return f'{self.__class__.__name__}: {self.message}'
