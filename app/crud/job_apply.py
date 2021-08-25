from sqlalchemy.orm import Session, relationship
from datetime import date, time,datetime
from sqlalchemy.sql.functions import mode
import models, schemas
from fastapi import HTTPException


def get_job_apply_by_account(db: Session, username: str):
    user = db.query(models.Account).filter(models.Account.username == username, models.Account.status != 0).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    resume_id_lst = []
    rs = db.query(models.Account,models.Resume).filter(models.Account.username == username, models.Account.username == models.Resume.create_by).all()
    for a,r in rs:
        resume_id_lst.append(r.id)
    rs = db.query(models.Job_apply).filter(models.Job_apply.id_resume.in_(resume_id_lst)).all()
    jobs = db.query(models.Job_post).filter(models.Job_post.id.in_([el.id_job for el in rs])).all()
    return jobs

def get_job_apply_by_resume(db: Session, resume_id: int):
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id, models.Resume.status != 0).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    job_applies = db.query(models.Job_apply).filter(models.Job_apply.id_resume == resume_id).all()
    jobs = db.query(models.Job_post).filter(models.Job_post.id.in_([el.id_job for el in job_applies])).all()
    return jobs

def get_resume_apply_to_job(db:Session, job_id: int):
    job = db.query(models.Job_post).filter(models.Job_post.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    job_applies = db.query(models.Job_apply).filter(models.Job_apply.id_job == job_id).all()
    resumes = db.query(models.Resume).filter(models.Resume.id.in_([el.id_resume for el in job_applies])).all()
    return resumes

def get_account_apply_to_job(db:Session, job_id: int):
    job = db.query(models.Job_post).filter(models.Job_post.id == job_id, models.Job_post.status != 0).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    job_applies = db.query(models.Job_apply).filter(models.Job_apply.id_job == job_id).all()
    resumes = db.query(models.Resume).filter(models.Resume.id.in_([el.id_resume for el in job_applies])).all()
    accounts = db.query(models.Account).filter(models.Account.username.in_([el.create_by for el in resumes]), models.Account.status != 0 ).all()
    return accounts

def create_job_apply(db:Session, apply_job: schemas.Job_apply_Create):
    apply_job_dic = dict(apply_job)
    job = db.query(models.Job_post).filter(models.Job_post.id == apply_job_dic['id_job'], models.Job_post.status != 0).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    now = datetime.now()
    if job.submit_expired_time < now.date():
        raise HTTPException(status_code=404, detail="Time expired")
    resume = db.query(models.Resume).filter(models.Resume.id == apply_job_dic["id_resume"], models.Resume.status != 0).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    job_apply = db.query(models.Job_apply).filter(models.Job_apply.id_job == apply_job_dic['id_job'],models.Job_apply.id_resume == apply_job_dic['id_resume']).first()
    if job_apply != None:
        raise HTTPException(status_code=404, detail="You have applied for this job")
    now = datetime.now()
    db_apply_job = models.Job_apply(**apply_job.dict())
    db_apply_job.time = now.strftime("%Y-%m-%d %H:%M:%S")
    db.add(db_apply_job)
    db.commit()
    db.refresh(db_apply_job)
    return db_apply_job

def unapply_job(db: Session, job_id:int, resume_id:int):
    job = db.query(models.Job_post).filter(models.Job_post.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    job_apply = db.query(models.Job_apply).filter(models.Job_apply.id_job == job_id, models.Job_apply.id_resume == resume_id).first()
    if job_apply:
        job_apply.status = 0
        db.commit()
        db.refresh(job_apply)
    else:
        raise HTTPException(status_code=404, detail="Job_apply not found")

