from sqlalchemy.orm import Session
from datetime import date, time,datetime
from sqlalchemy.sql.functions import mode
import models, schemas
from fastapi import HTTPException


def get_account_job_mark(db: Session, username: str):
    return db.query(models.Job_mark).filter(models.Job_mark.by_account == username, models.Job_mark.status != 0).all()

def get_account_job_mark_with_job(db: Session, username: str,job_id: int):
    return db.query(models.Job_mark).filter(models.Job_mark.by_account == username,models.Job_mark.id_job == job_id, models.Job_mark.status != 0).first()


def account_job_unmark(db: Session, username:str, job_id: int):
    job_mark = db.query(models.Job_mark).filter(models.Job_mark.id_job == job_id,models.Job_mark.by_account == username).first()
    if job_mark:
        job_mark.status = 0
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Not exist mark")
    return job_mark

def account_job_mark(db:Session, username:str, job_id:int):
    job_mark = db.query(models.Job_mark).filter( models.Job_mark.by_account == username, models.Job_mark.id_job == job_id).first()
    if job_mark:
        raise HTTPException(status_code=404, detail="Marked before")
    else:
        now = datetime.now()
        job_mark = models.Job_mark(id_job=job_id, by_account=username,status=1,time= now.strftime("%Y-%m-%d %H:%M:%S"))
        db.add(job_mark)
        db.commit()
        db.refresh(job_mark)
    return job_mark

