from fastapi import APIRouter,Depends,status,Response,HTTPException,Security
from router import oauth2
from typing import Optional
from datetime import date,datetime
from typing import List
import schemas,database
from crud import job_mark

router =  APIRouter(
    tags = ["Job_mark"], 
    prefix = "/job_mark"
)


@router.get("/mark/me", response_model= List[schemas.Job_mark])
def read_account_job_mark(db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_job_mark = job_mark.get_account_job_mark(db, username= current_user.username)
    return db_job_mark

@router.get("/mark/me/{job_id}", response_model= schemas.Job_mark)
def read_account_job_mark_with_job(job_id: int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_job_mark = job_mark.get_account_job_mark_with_job(db, username= current_user.username,job_id= job_id)
    if db_job_mark is None:
        raise HTTPException(status_code=404, detail="job_mark not found")
    return db_job_mark

@router.put("/unmark/me/{job_id}", response_model= schemas.Job_mark)
def account_job_unmark(job_id: int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_job_mark = job_mark.account_job_unmark(db, username= current_user.username,job_id= job_id)
    return db_job_mark

@router.post("/mark/me/{job_id}", response_model= schemas.Job_mark)
def account_job_mark(job_id: int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_job_mark = job_mark.account_job_mark(db=db, username= current_user.username, job_id=job_id)
    return db_job_mark

