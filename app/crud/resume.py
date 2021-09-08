from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import models, schemas
from datetime import datetime
from fastapi import HTTPException

def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resume).offset(skip).limit(limit).all()

def get_resumes_for_user(db: Session,username: str):
    account = db.query(models.Account).filter(models.Account.username == username, models.Account.status != 0).first()
    if account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(models.Resume).filter(models.Resume.create_by == username,models.Resume.status != 0).all()

def get_resume_by_id(db:Session, resume_id: int):
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    return resume

def get_resume_by_username(db:Session, username: str):
    acc = db.query(models.Account).filter(models.Account.username == username, models.Account.status != 0).first()
    if acc is None:
        raise HTTPException(status_code=404, detail="Username not found")
    resume = db.query(models.Resume).filter(models.Resume.create_by == username).all()
    return resume

def create_account_resume(db: Session, resume: schemas.Resume_Create, username: str):
    acc = db.query(models.Account).filter(models.Account.username == username,models.Account.status != 0).first()
    if acc is None:
        raise HTTPException(status_code=404, detail="Username not found")
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

def update_resume_by_id(resume: schemas.Resume_Create,db:Session,resume_id:int):
    db_resume = db.query(models.Resume).filter(models.Resume.id == resume_id,models.Resume.status != 0).first()
    if db_resume != None:
        resume_dic = dict(resume)
        db.query(models.Resume).filter(models.Resume.id == resume_id,models.Resume.status != 0).update(resume_dic)
        db.commit()
        db.refresh(db_resume)
    else:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume