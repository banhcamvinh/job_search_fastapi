from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import List
import schemas,database
from crud import account_rating

router =  APIRouter(
    tags = ["Account_rating"], 
    prefix = "/account_rating"
)

@router.get("/{username}", response_model=schemas.Account_rating)
def read_account_rating(username: str, db: database.Session = Depends(database.get_db)):
    db_account_rating = account_rating.get_account_rating(db, username= username)
    if db_account_rating is None:
        raise HTTPException(status_code=404, detail="Empty")
    return db_account_rating