from sqlalchemy import Column, DateTime, Integer, String, Text, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class AppealModel(Base):
    __tablename__ = "appeal"
    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    phone_number = Column(BigInteger)
    description = Column(Text)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
