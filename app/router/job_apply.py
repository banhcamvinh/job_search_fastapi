from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import Optional
from datetime import date,datetime
from typing import List
import schemas,database
from crud import job_apply,resume

router =  APIRouter(
    tags = ["Job_apply"], 
    prefix = "/job_apply"
)

@router.get("/job_by_account/{username}", response_model= List[schemas.Job_post])
def read_job_apply_by_account(username: str, db: database.Session = Depends(database.get_db)):
    db_job = job_apply.get_job_apply_by_account(db, username= username)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Empty")
    return db_job

@router.get("/job_by_resume/{resume_id}", response_model= List[schemas.Job_post])
def get_job_apply_by_resume(resume_id: int, db: database.Session = Depends(database.get_db)):
    db_jobs = job_apply.get_job_apply_by_resume(db=db, resume_id= resume_id)
    if db_jobs is None:
        raise HTTPException(status_code=404, detail="Empty")
    return db_jobs

@router.get("/resume_to_job/{job_id}", response_model= List[schemas.Resume])
def get_resume_apply_to_job(job_id: int, db: database.Session = Depends(database.get_db)):
    db_resumes = job_apply.get_resume_apply_to_job(db=db, job_id=job_id)
    if db_resumes is None:
        raise HTTPException(status_code=404, detail="Empty")
    return db_resumes

@router.get("/account_to_job/{job_id}", response_model= List[schemas.Account_Info])
def get_account_apply_to_job(job_id: int, db: database.Session = Depends(database.get_db)):
    db_account = job_apply.get_account_apply_to_job(db=db, job_id=job_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Empty")
    return db_account

@router.post("", response_model = schemas.Job_apply)
def creat_job_apply(job_apply_in: schemas.Job_apply_Create,db:database.Session = Depends(database.get_db)):
    job_apply_db = job_apply.create_job_apply(db=db,apply_job=job_apply_in)
    return job_apply_db

@router.put("/unapply/{job_id}/{resume_id}",response_model= schemas.Job_apply)
def unapply_job(job_id: int, resume_id: int, db:database.Session = Depends(database.get_db)):
    job_apply_db = job_apply.unapply_job(db=db,job_id=job_id,resume_id=resume_id)
    return job_apply_db
    


# @router.get("/mark/{username}/{job_id}", response_model= schemas.Job_apply)
# def read_account_job_apply_with_job(username: str,job_id: int, db: database.Session = Depends(database.get_db)):
#     db_resumes = job_apply.get_account_job_apply_with_job(db, username= username,job_id= job_id)
#     if db_job_apply is None:
#         raise HTTPException(status_code=404, detail="Empty")
#     return db_job_apply

# @router.put("/unmark/{username}/{job_id}", response_model= schemas.Job_apply)
# def account_job_unmark(username: str,job_id: int, db: database.Session = Depends(database.get_db)):
#     db_job_apply = job_apply.account_job_unmark(db, username= username,job_id= job_id)
#     return db_job_apply

# @router.post("/mark/{username}/{job_id}", response_model= schemas.Job_apply)
# def account_job_apply(username: str,job_id: int, db: database.Session = Depends(database.get_db)):
#     db_job_apply = job_apply.account_job_apply(db=db, username=username, job_id=job_id)
#     return db_job_apply

