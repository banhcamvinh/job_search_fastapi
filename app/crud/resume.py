from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import models, schemas
from fastapi import HTTPException

def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resume).offset(skip).limit(limit).all()

def get_resumes_for_user(db: Session,username: str):
    account = db.query(models.Account).filter(models.Account.username == username).first()
    if account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(models.Resume).filter(models.Resume.create_by == username).all()

def get_resume_by_id(db:Session, resume_id: int):
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    return resume

def get_resume_by_username(db:Session, username: str):
    resume = db.query(models.Resume).filter(models.Resume.create_by == username).all()
    return resume

def create_account_resume(db: Session, resume: schemas.Resume_Create, username: str):
    db_resume = models.Resume(**resume.dict(), create_by=username)
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def accept_resume(db: Session, resume_id: int):
    db_resume= db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if db_resume:
        db_resume.status = 1
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Resume not found")

def disable_resume(db: Session, resume_id: int):
    db_resume= db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if db_resume:
        db_resume.status = 0
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Resume not found")
