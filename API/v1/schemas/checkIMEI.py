from pydantic import BaseModel


class HelloScheme(BaseModel):
    message: str
