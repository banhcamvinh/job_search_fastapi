from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import List, Optional
import schemas,database
from crud import job_post

router =  APIRouter(
    tags = ["Job_post"], 
    prefix = "/job_posts"
)

@router.get("", response_model=List[schemas.Job_post])
def read_job_posts(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db)):
    job_posts = job_post.get_job_posts(db, skip=skip, limit=limit)
    return job_posts

@router.get("/filter", response_model= List[schemas.Job_post])
def read_job_post_by_title(title: Optional[str]=None, position: Optional[str]=None,skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db)):
    params= locals().copy()
    filter_dict={}
    for el in params:
        if el != "skip" and el != "limit" and el != "db" and params[el] != None:
            filter_dict[el] = params[el]
    job_posts = job_post.get_job_posts_filter(filters=filter_dict,db= db,skip=skip,limit=limit)
    return job_posts

@router.post("/{username}/{id_company}", response_model=schemas.Job_post)
def create_job_post(username: str,id_company: int, Job_post: schemas.Job_post_Create, db: database.Session = Depends(database.get_db)):
    return job_post.create_job_post(db=db, job_post = Job_post, username = username, id_company= id_company)
