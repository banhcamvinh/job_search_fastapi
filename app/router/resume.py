from fastapi import APIRouter,Depends,status,Response,HTTPException,Security
from router import oauth2
from typing import List
import schemas,database
from crud import resume

router =  APIRouter(
    tags = ["Resume"], 
    prefix = "/resumes"
)

@router.get("", response_model=List[schemas.Resume_Admin])
def read_resumes_for_admin(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db), current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    resumes = resume.get_resumes(db, skip=skip, limit=limit)
    return resumes

@router.get("/id/{resume_id}",response_model=schemas.Resume_Admin)
def read_resume_by_id_for_admin(resume_id: int,db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    resume_db = resume.get_resume_by_id(db=db, resume_id = resume_id)
    if resume_db is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume_db

@router.get("/username/{username}",response_model=List[schemas.Resume_Admin])
def read_resume_by_username_for_admin(username: str,db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    resume_db = resume.get_resume_by_username(db=db, username = username)
    if resume_db is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume_db

@router.get("/me", response_model=List[schemas.Resume])
def read_resumes_for_user( db: database.Session = Depends(database.get_db), current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    resumes = resume.get_resumes_for_user(db, username= current_user.username)
    return resumes

@router.post("/me", response_model=schemas.Resume)
def create_resume_for_user( Resume: schemas.Resume_Create, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    return resume.create_account_resume(db=db, resume=Resume, username= current_user.username)

@router.put("/accept/{resume_id}",status_code=200)
def accept_resume(resume_id: int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    resume.accept_resume(db=db, resume_id= resume_id)
    return {"message":"success"}

@router.put("/disable/{resume_id}",status_code=200)
def disable_resume(resume_id: int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    resume.disable_resume(db=db, resume_id= resume_id)
    return {"message":"success"}
