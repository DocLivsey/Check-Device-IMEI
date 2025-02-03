from pydantic import BaseModel


class HelloScheme(BaseModel):
    message: str


def to_message(message: str) -> HelloScheme:
    if not message:
        message = 'Undefined'

    return HelloScheme(message=message)
