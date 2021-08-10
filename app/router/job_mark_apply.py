from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import List
import schemas,database
from crud import job_mark_apply

router =  APIRouter(
    tags = ["Job_mark_apply"], 
    prefix = "/job_mark_apply"
)

@router.get("/{username}", response_model=schemas.Job_mark_apply)
def read_account_job_mark_apply(username: str, db: database.Session = Depends(database.get_db)):
    db_job_mark_apply = job_mark_apply.get_account_job_mark_apply(db, username= username)
    if db_job_mark_apply is None:
        raise HTTPException(status_code=404, detail="Empty")
    return db_job_mark_apply