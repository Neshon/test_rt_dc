from pydantic import BaseModel


class AppealSchema(BaseModel):
    surname: str
    name: str
    patronymic: str
    phone_number: int
    description: str

    class Config:
        orm_mode = True
