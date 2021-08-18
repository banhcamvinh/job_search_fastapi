from typing import List
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import models, schemas
from fastapi import HTTPException

def get_job_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job_post).filter(models.Job_post.status != 0).offset(skip).limit(limit).all()

def get_job_posts_by_id(job_post_id:int,db: Session):
    job_post = db.query(models.Job_post).filter(models.Job_post.id == job_post_id).filter(models.Job_post.status != 0).first()
    if job_post is None:
        raise HTTPException(status_code=404, detail="User not found")
    return job_post

def create_job_post(db: Session, job_post: schemas.Job_post_Create, username: str, id_company: int):
    user = db.query(models.Account).filter(models.Account.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    company = db.query(models.Company).filter(models.Company.id == id_company).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    db_job_post = models.Job_post(**job_post.dict(), posted_by=username,about_company= id_company)
    now = datetime.now()
    expired_time = now + timedelta(weeks=4)
    db_job_post.expired_time = expired_time
    db_job_post.create_time = now.strftime("%Y/%m/%d %H:%M:%S")
    db_job_post.update_time = db_job_post.create_time
    db.add(db_job_post)
    db.commit()
    db.refresh(db_job_post)
    return db_job_post

def get_job_posts_filter(filters:dict,db: Session, skip: int = 0, limit: int = 100):
    job_posts = db.query(models.Job_post)
    for attr,val in filters.items():
        job_posts= job_posts.filter(getattr(models.Job_post,attr).ilike('%{}%'.format(val))).filter(models.Job_post.status != 0)
    return job_posts.all()
        
def update_job_post_by_id(job_post: schemas.Job_post_Create,db:Session,job_post_id:int):
    db_job_post = db.query(models.Job_post).filter(models.Job_post.id == job_post_id,models.Job_post.status != 0).first()
    if db_job_post != None:
        job_post_dic = dict(job_post)
        now = datetime.now()
        db_job_post.update_time = now.strftime("%Y/%m/%d %H:%M:%S")
        db.query(models.Job_post).update(job_post_dic)
        db.commit()
        db.refresh(db_job_post)
    else:
        raise HTTPException(status_code=404, detail="Job_post not found")
    return db_job_post
        
def disable_job_post_by_id(db:Session,job_post_id:int):
    db_job_post = db.query(models.Job_post).filter(models.Job_post.id == job_post_id).filter(models.Job_post.status != 0).first()
    if db_job_post != None:
        db_job_post.status = 0
        db.commit()
        db.refresh(db_job_post)
    else:
        raise HTTPException(status_code=404, detail="Job_post not found")

def increase_job_post_view(db: Session,job_post_id: int):
    db_job_post = db.query(models.Job_post).filter(models.Job_post.id == job_post_id).first()
    if db_job_post != None:
        db_job_post.view += 1
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Job post not found")

def accept_job_post_by_id(db:Session, job_post_id: int):
    db_job_post = db.query(models.Job_post).filter(models.Job_post.id == job_post_id).first()
    if db_job_post != None:
        db_job_post.status = 1
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Job_post not found")

def change_job_post__mode_by_id(db:Session, job_post_id: int,mode: int):
    db_job_post = db.query(models.Job_post).filter(models.Job_post.id == job_post_id).first()
    if db_job_post != None:
        db_job_post.mode = mode
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Job_post not found")