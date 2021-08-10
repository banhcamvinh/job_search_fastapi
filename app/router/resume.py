from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import List
import schemas,database
from crud import resume

router =  APIRouter(
    tags = ["Resume"], 
    prefix = "/resumes"
)

@router.get("", response_model=List[schemas.Resume])
def read_resumes(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db)):
    resumes = resume.get_resumes(db, skip=skip, limit=limit)
    return resumes

@router.post("/accounts/{username}", response_model=schemas.Resume)
def create_resume_for_user(username: str, Resume: schemas.Resume_Create, db: database.Session = Depends(database.get_db)):
    return resume.create_account_resume(db=db, resume=Resume, username=username)
