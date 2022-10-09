from pydantic import BaseModel, Field


class User(BaseModel):

    id: str
    name: str
    email_address: str


class Response(BaseModel):

    message: str
