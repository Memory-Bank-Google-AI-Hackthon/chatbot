from pydantic import BaseModel


class SaveMessage(BaseModel):
    message: str
    images: list[str] = []
    urls: list[str] = []
