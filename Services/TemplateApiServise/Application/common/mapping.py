from typing import Union, Type, cast

from pydantic import BaseModel

from Services.TemplateApiServise.Domain.BaseEntity import Base


def mapping(from_data: Union[BaseModel | dict | object], to: Type[Base]):
    if isinstance(from_data, object):
        from_data = from_data.__dict__
    elif isinstance(from_data, BaseModel):
        from_data = from_data.model_dump()

    assert isinstance(from_data, dict), 'from_data must be a dict'

    return cast(to, to(**from_data))
