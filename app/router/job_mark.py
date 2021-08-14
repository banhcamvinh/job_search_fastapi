from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import Optional
from datetime import date,datetime
from typing import List
import schemas,database
from crud import job_mark

router =  APIRouter(
    tags = ["Job_mark"], 
    prefix = "/job_mark"
)


@router.get("/mark/{username}", response_model= List[schemas.Job_mark])
def read_account_job_mark(username: str, db: database.Session = Depends(database.get_db)):
    db_job_mark = job_mark.get_account_job_mark(db, username= username)
    if db_job_mark is None:
        raise HTTPException(status_code=404, detail="Empty")
    return db_job_mark


@router.get("/mark/{username}/{job_id}", response_model= schemas.Job_mark)
def read_account_job_mark_with_job(username: str,job_id: int, db: database.Session = Depends(database.get_db)):
    db_job_mark = job_mark.get_account_job_mark_with_job(db, username= username,job_id= job_id)
    if db_job_mark is None:
        raise HTTPException(status_code=404, detail="Empty")
    return db_job_mark

@router.put("/unmark/{username}/{job_id}", response_model= schemas.Job_mark)
def account_job_unmark(username: str,job_id: int, db: database.Session = Depends(database.get_db)):
    db_job_mark = job_mark.account_job_unmark(db, username= username,job_id= job_id)
    return db_job_mark

@router.post("/mark/{username}/{job_id}", response_model= schemas.Job_mark)
def account_job_mark(username: str,job_id: int, db: database.Session = Depends(database.get_db)):
    db_job_mark = job_mark.account_job_mark(db=db, username=username, job_id=job_id)
    return db_job_mark

