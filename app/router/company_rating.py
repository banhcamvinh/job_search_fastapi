from sqlalchemy.sql import schema
from fastapi import APIRouter,Depends,status,Response,HTTPException,Security
from typing import List
from datetime import datetime
import schemas,database
from crud import company_rating
from router import oauth2

router =  APIRouter(
    tags = ["Company_rating"], 
    prefix = "/company_rating"
)

@router.get("/{company_id}", response_model= List[schemas.Company_rating])
def read_company_rating(company_id: int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_company_rating = company_rating.get_company_rating(db, company_id= company_id)
    return db_company_rating

@router.get("/{username}/{company_id}/{time}", response_model= schemas.Company_rating)
def read_company_rating_detail(username: str,company_id : int, time: datetime, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_company_rating = company_rating.get_company_rating_detail(db, username= username, company_id= company_id, time=time)
    if db_company_rating is None:
        raise HTTPException(status_code=404, detail="Company rating not found")
    return db_company_rating

@router.post("", response_model= schemas.Company_rating)
def create_cpmpany_rating(company_rating_in: schemas.Company_rating_Create, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_company_rating = company_rating.create_company_rating(db, company_rating_in)
    return db_company_rating

@router.delete("/{username}/{company_id}/{time}",status_code =200)
def delete_company_rating(username: str, company_id: int, time: datetime, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    company_rating.delete_company_rating_detail(db, username= username, company_id= company_id, time=time)
    return "success"

@router.put("", response_model= schemas.Company_rating)
def edit_company_rating(company_rating_in: schemas.Company_rating_time, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_company_rating = company_rating.edit_company_rating(db, company_rating_in)
    if db_company_rating is None:
        raise HTTPException(status_code=404, detail="company rating not found")
    return db_company_rating

@router.put("/hide/{username}/{company_id}/{time}", status_code = 200)
def hide_company_rating(username: str, company_id: int, time: datetime, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    company_rating.hide_company_rating(db=db, username= username, company_id=company_id, time=time)
    return {"Message":"Success"}

