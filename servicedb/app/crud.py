from .schemas import AppealSchema
from .models import AppealModel


def create_appeal(db, appeal: AppealSchema):
    db_appeal = AppealModel(**appeal.dict())
    db.add(db_appeal)
    db.commit()
    db.refresh(db_appeal)
    return db_appeal
