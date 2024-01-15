from pydantic import BaseModel


class PageConfig(BaseModel):
    size: str = "A4"
    margin: int | tuple[int, int, int, int] = 0
    orientation: str = "portrait"
