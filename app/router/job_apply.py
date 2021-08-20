from fastapi import APIRouter,Depends,status,Response,HTTPException,Security
from typing import Optional
from datetime import date,datetime
from typing import List
import schemas,database
from crud import job_apply,resume,job_post
from router import oauth2

router =  APIRouter(
    tags = ["Job_apply"], 
    prefix = "/job_apply"
)

@router.get("/job_by_account/me", response_model= List[schemas.Job_post])
def read_job_apply_by_account( db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_job = job_apply.get_job_apply_by_account(db, username= current_user.username)
    return db_job

@router.get("/job_by_resume/{resume_id}", response_model= List[schemas.Job_post])
def get_job_apply_by_resume(resume_id: int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_jobs = job_apply.get_job_apply_by_resume(db=db, resume_id= resume_id)
    return db_jobs

@router.get("/resume_to_job/{job_id}", response_model= List[schemas.Resume])
def get_resume_apply_to_job(job_id: int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_resumes = job_apply.get_resume_apply_to_job(db=db, job_id=job_id)
    return db_resumes

@router.get("/account_to_job/{job_id}", response_model= List[schemas.Account_Info])
def get_account_apply_to_job(job_id: int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_account = job_apply.get_account_apply_to_job(db=db, job_id=job_id)
    return db_account

@router.post("", response_model = schemas.Job_apply)
def create_job_apply(job_apply_in: schemas.Job_apply_Create,db:database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    job_apply_db = job_apply.create_job_apply(db=db,apply_job=job_apply_in)
    job = job_post.get_job_posts_by_id(job_apply_db.id_job)
    return job_apply_db

@router.put("/unapply/{job_id}/{resume_id}")
def unapply_job(job_id: int, resume_id: int, db:database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    job_apply.unapply_job(db=db,job_id=job_id,resume_id=resume_id)
    return {"Message":"Success"}
    