from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import models, schemas

def get_job_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job_post).offset(skip).limit(limit).all()

def create_job_post(db: Session, job_post: schemas.Job_post_Create, username: str, id_company: int):
    db_job_post = models.Job_post(**job_post.dict(), posted_by=username,about_company= id_company)
    db.add(db_job_post)
    db.commit()
    db.refresh(db_job_post)
    return db_job_post

def get_job_posts_filter(filters:dict,db: Session, skip: int = 0, limit: int = 100):
    job_posts = db.query(models.Job_post)
    for attr,val in filters.items():
        print(val)
        job_posts= job_posts.filter(getattr(models.Job_post,attr).ilike('%{}%'.format(val)))
    return job_posts.all()
        
