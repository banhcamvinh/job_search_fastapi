from datetime import datetime
from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import List
import schemas,database
from crud import account_rating

router =  APIRouter(
    tags = ["Account_rating"], 
    prefix = "/account_rating"
)

@router.get("/{username}", response_model= List[schemas.Account_rating])
def read_account_rating(username: str, db: database.Session = Depends(database.get_db)):
    db_account_rating = account_rating.get_account_rating(db, username= username)
    if db_account_rating is None:
        raise HTTPException(status_code=404, detail="Empty")
    return db_account_rating

@router.get("/{who}/{towhom}/{time}", response_model= schemas.Account_rating)
def read_account_rating_detail(who: str,towhom: str, time: datetime, db: database.Session = Depends(database.get_db)):
    db_account_rating = account_rating.get_account_rating_detail(db, who= who, towhom=towhom, time=time)
    if db_account_rating is None:
        raise HTTPException(status_code=404, detail="Empty")
    return db_account_rating

@router.post("", response_model= schemas.Account_rating)
def create_account_rating(account_rating_in: schemas.Account_rating_Create, db: database.Session = Depends(database.get_db)):
    db_account_rating = account_rating.create_account_rating(db, account_rating_in)
    return db_account_rating

@router.delete("/{who}/{towhom}/{time}")
def delete_account_rating(who: str,towhom: str, time: datetime, db: database.Session = Depends(database.get_db)):
    account_rating.delete_account_rating_detail(db, who= who, towhom=towhom, time=time)
    return "success"

@router.put("", response_model= schemas.Account_rating)
def edit_account_rating(account_rating_in: schemas.Account_rating_time, db: database.Session = Depends(database.get_db)):
    db_account_rating = account_rating.edit_account_rating(db, account_rating_in)
    return db_account_rating

@router.put("/hide/{who}/{towhom}/{time}", response_model= schemas.Account_rating)
def hide_account_rating(who: str, towhom: str, time: datetime, db: database.Session = Depends(database.get_db)):
    db_account_rating = account_rating.hide_account_rating(db=db, who=who, towhom=towhom, time=time)
    return db_account_rating

