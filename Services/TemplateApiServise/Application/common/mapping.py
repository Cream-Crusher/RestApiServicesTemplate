from typing import Union, Type, cast

from Services.TemplateApiServise.Domain.BaseEntity import BaseEntity


def mapping(from_data: Union[BaseEntity | dict | object], to: Type[BaseEntity]):
    if isinstance(from_data, object):
        from_data = from_data.__dict__
    elif isinstance(from_data, BaseEntity):
        from_data = from_data.model_dump()

    assert isinstance(from_data, dict), 'from_data must be a dict'

    return cast(to, to(**from_data))
