from pydantic import BaseModel


class AppealBase(BaseModel):
    surname: str
    name: str
    patronymic: str
    phone_number: int
    description: str

    class Config:
        orm_mode = True
