from router import oauth2
from crud import account
from fastapi import APIRouter,Depends,status,Response,HTTPException,Security
from typing import List
import schemas,database

router =  APIRouter(
    tags = ["Account"],
    prefix = "/accounts"
)

@router.get("/{username}", response_model=schemas.Account)
def read_account(username: str, db: database.Session = Depends(database.get_db), current_user: schemas.Account = Security(oauth2.get_current_user, scopes=["1"])):
    db_account = account.get_account(db, username= username)
    if db_account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_account

@router.get( "",response_model=List[schemas.Account])
def read_accounts(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db)):
    accounts = account.get_accounts(db, skip=skip, limit=limit)
    return accounts

@router.post( "",response_model=schemas.Account)
def create_account(accounts: schemas.Account_create, db: database.Session = Depends(database.get_db)):
    db_account = account.get_account(db, username= accounts.username)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return account.create_account(db,accounts)
