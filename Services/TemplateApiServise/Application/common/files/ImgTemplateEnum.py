import pathlib
from collections.abc import Iterable
from enum import Enum, nonmember

FULL_PATH = pathlib.Path(__file__).parent.resolve()


class ImgTemplateEnum(Enum):
    img_0 = (0, "img_1.png", "tag_1")
    img_1 = (1, "img_2.png", "tag_2")

    _index = nonmember({})

    def __init__(self, id: int, filename: str, tag: str) -> None:
        self.id = id
        self.filename = filename
        self.bytes_data = self._load_image(filename)
        self.tag = tag

        assert self.id not in self._index
        self._index[self.id] = self
        super().__init__()

    @classmethod
    def get(cls, id: int) -> "ImgTemplateEnum":
        return cls._index[id]

    @classmethod
    def get_by_tag(cls, tag: str) -> "ImgTemplateEnum":
        return next((item for item in cls._index.values() if item.tag == tag), None)

    @classmethod
    def iter(cls) -> Iterable["ImgTemplateEnum"]:
        yield from cls._index.values()

    @staticmethod
    def _load_image(filename: str) -> bytes:
        with open(f"{FULL_PATH}/{filename}", "rb") as f:
            return f.read()
