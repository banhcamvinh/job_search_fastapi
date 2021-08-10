from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import models, schemas

def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resume).offset(skip).limit(limit).all()

def create_account_resume(db: Session, resume: schemas.Resume_Create, username: str):
    db_resume = models.Resume(**resume.dict(), create_by=username)
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume
