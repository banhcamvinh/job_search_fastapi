from datetime import datetime
from fastapi import APIRouter,Depends,status,Response,HTTPException,Security
from typing import List
import schemas,database
from crud import account_rating
from router import oauth2

router =  APIRouter(
    tags = ["Account_rating"], 
    prefix = "/account_rating"
)

@router.get("/{username}", response_model= List[schemas.Account_rating])
def read_account_rating(username: str, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_account_rating = account_rating.get_account_rating(db, username= username)
    return db_account_rating

@router.get("/{who}/{towhom}/{time}", response_model= schemas.Account_rating)
def read_account_rating_detail(who: str,towhom: str, time: datetime, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_account_rating = account_rating.get_account_rating_detail(db, who= who, towhom=towhom, time=time)
    if db_account_rating is None:
        raise HTTPException(status_code=404, detail="Account rating not found")
    return db_account_rating

@router.post("", response_model= schemas.Account_rating)
def create_account_rating(account_rating_in: schemas.Account_rating_Create, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_account_rating = account_rating.create_account_rating(db, account_rating_in)
    return db_account_rating

@router.delete("/{who}/{towhom}/{time}",status_code = 200)
def delete_account_rating(who: str,towhom: str, time: datetime, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    account_rating.delete_account_rating_detail(db, who= who, towhom=towhom, time=time)
    return "success"

@router.put("", response_model= schemas.Account_rating)
def edit_account_rating(account_rating_in: schemas.Account_rating_time, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_account_rating = account_rating.edit_account_rating(db, account_rating_in)
    if db_account_rating is None:
        raise HTTPException(status_code=404, detail="account rating not found")
    return db_account_rating

@router.put("/hide/{who}/{towhom}/{time}", status_code = 200)
def hide_account_rating(who: str, towhom: str, time: datetime, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    account_rating.hide_account_rating(db=db, who=who, towhom=towhom, time=time)
    return {"Message":"Success"}

