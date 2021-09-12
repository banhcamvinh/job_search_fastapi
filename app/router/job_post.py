from fastapi import APIRouter,Depends,status,Response,HTTPException,Security
from router import oauth2
from typing import List, Optional
import schemas,database
from crud import job_post

router =  APIRouter(
    tags = ["Job_post"], 
    prefix = "/job_posts"
)

@router.get("", response_model=List[schemas.Job_post])
def read_job_posts(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    job_posts = job_post.get_job_posts(db, skip=skip, limit=limit)
    return job_posts

@router.get("/me/active", response_model=List[schemas.Job_post])
def read_job_posts_me_active(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    job_posts = job_post.get_job_posts_me_active(db=db, skip=skip, limit=limit,username= current_user.username)
    return job_posts

@router.get("/me/inactive", response_model=List[schemas.Job_post])
def read_job_posts_me_inactive(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    job_posts = job_post.get_job_posts_me_inactive(db=db, skip=skip, limit=limit,username= current_user.username)
    return job_posts

@router.get("/me/all", response_model=List[schemas.Job_post])
def read_job_posts_me_all(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    job_posts = job_post.get_job_posts_me_all(db=db, skip=skip, limit=limit,username= current_user.username)
    return job_posts

@router.get("/applicants", response_model=List[schemas.Job_post])
def read_job_posts_me_applicants(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    job_posts = job_post.get_job_with_applicants(db, skip=skip, limit=limit,username= current_user.username)
    return job_posts


@router.get("/inactive", response_model=List[schemas.Job_post])
def read_job_posts_inactive(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    job_posts = job_post.get_job_posts_inactive(db, skip=skip, limit=limit)
    return job_posts


@router.get("/filter", response_model= List[schemas.Job_post])
def read_job_post_by_filter(title: Optional[str]=None, position: Optional[str]=None, location:Optional[str]=None, type:Optional[str]=None, skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    params= locals().copy()
    filter_dict={}
    for el in params:
        if el != "skip" and el != "limit" and el != "db" and el != "current_user" and params[el] != None:
            filter_dict[el] = params[el]
    job_posts = job_post.get_job_posts_filter(filters=filter_dict,db= db,skip=skip,limit=limit)
    return job_posts

@router.get("/{job_post_id}", response_model = schemas.Job_post)
def read_job_post_by_id(job_post_id:int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    job_post.increase_job_post_view(db=db, job_post_id= job_post_id)
    return job_post.get_job_posts_by_id(job_post_id= job_post_id,db=db)

@router.post("/{username}/{id_company}", response_model=schemas.Job_post)
def create_job_post(username: str,id_company: int, Job_post: schemas.Job_post_Create, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    return job_post.create_job_post(db=db, job_post = Job_post, username = username, id_company= id_company)

@router.put("/update/{job_post_id}",response_model = schemas.Job_post)
def update_job_post_by_id(job_post_id:int,Job_post: schemas.Job_post_Create, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    return job_post.update_job_post_by_id(db=db,job_post_id=job_post_id,job_post=Job_post)

@router.put("/disable/{job_post_id}", status_code = 200)
def disable_job_post_by_id(job_post_id:int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user)):
    job_post.disable_job_post_by_id(db=db,job_post_id=job_post_id)
    return {"Message":"Success"}

@router.put("/accept/{job_post_id}", status_code = 200)
def accept_job_post_by_id(job_post_id:int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    job_post.accept_job_post_by_id(db=db,job_post_id=job_post_id)
    return {"Message":"Success"}
    
@router.put("/mode/{job_post_id}/{mode}",status_code = 200)
def change_job_post_mode_by_id(job_post_id:int,mode: int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    job_post.change_job_post__mode_by_id(db=db,job_post_id=job_post_id,mode=mode)
    return {"Message":"Success"}