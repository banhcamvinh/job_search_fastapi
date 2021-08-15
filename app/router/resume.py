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

@router.get("/{resume_id}",response_model=schemas.Resume)
def read_resume_by_id(resume_id: int,db: database.Session = Depends(database.get_db)):
    resume_db = resume.get_resume_by_id(db=db, resume_id = resume_id)
    return resume_db

@router.get("/username/{username}",response_model=List[schemas.Resume])
def read_resume_by_username(username: str,db: database.Session = Depends(database.get_db)):
    resume_db = resume.get_resume_by_username(db=db, username = username)
    return resume_db

@router.post("/{username}", response_model=schemas.Resume)
def create_resume_for_user(username: str, Resume: schemas.Resume_Create, db: database.Session = Depends(database.get_db)):
    return resume.create_account_resume(db=db, resume=Resume, username=username)

@router.put("/accept/{resume_id}")
def accept_resume(resume_id: int, db: database.Session = Depends(database.get_db)):
    resume.accept_resume(db=db, resume_id= resume_id)
    return "success"

@router.put("/disable/{resume_id}")
def disable_resume(resume_id: int, db: database.Session = Depends(database.get_db)):
    resume.disable_resume(db=db, resume_id= resume_id)
    return "success"
