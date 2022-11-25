from sqlalchemy import select
from sqlalchemy.orm import Session

from . import schemas
from .models import Appeal as AppealModel


def get_appeal(db: Session):
    appeal = select(AppealModel)
    return db.execute(appeal).scalars().all()


def create_appeal(db: Session, appeal: schemas.AppealBase):
    db_appeal = AppealModel(**appeal.dict())
    db.add(db_appeal)
    db.commit()
    db.refresh(db_appeal)
    return db_appeal