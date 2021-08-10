from router import oauth2
from crud import account
from fastapi import APIRouter,Depends,status,Response,HTTPException,Security
from typing import List
import schemas,database
import my_email
import string
import random


router =  APIRouter(
    tags = ["Account"],
    prefix = "/accounts"
)

@router.get("/me", response_model=schemas.Account)
def read_account_for_user( db: database.Session = Depends(database.get_db), current_user: schemas.Account = Depends(oauth2.get_current_user)):
    db_account = account.get_account(db, username= current_user.username)
    if db_account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_account

@router.post("/me/change_password",response_model=schemas.Account)
def change_account_password_for_user(accounts:schemas.Account_password, db: database.Session = Depends(database.get_db), current_user: schemas.Account = Depends(oauth2.get_current_user)):
    print("Test")
    db_account =  account.change_account_password(db, username= current_user.username,password= accounts.password)
    if db_account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_account

@router.get("/{username}", response_model=schemas.Account)
def read_account_for_admin(username: str, db: database.Session = Depends(database.get_db), current_user: schemas.Account = Security(oauth2.get_current_user, scopes=["1"])):
    db_account = account.get_account(db, username= username)
    if db_account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_account

@router.get( "",response_model=List[schemas.Account])
def read_accounts_list_for_admin(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db),current_user: schemas.Account = Security(oauth2.get_current_user, scopes=["1"])):
    accounts = account.get_accounts(db, skip=skip, limit=limit)
    return accounts

@router.get("/verify/{username}",response_model= schemas.Account)
def verify_account(username: str, db: database.Session = Depends(database.get_db)):
    db_account= account.accept_account(db,username=username)
    if db_account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_account

@router.post( "",response_model=schemas.Account)
def create_account(accounts: schemas.Account_create, db: database.Session = Depends(database.get_db)):
    db_account = account.get_account(db, username= accounts.username)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")

    content="""\
    <html>
    <body>
        <p>Hi,<br>
        Please click the button below to verify your account on our platform <br>
        <a href="http://127.0.0.1:8000/accounts/verify/{}">Click here</a> <br>
        Best regards
        </p>
    </body>
    </html>
    """.format(accounts.username)
    my_email.send_email(accounts.username,"Verification Email for register our platform",content)

    return account.create_account(db,accounts)

@router.post("/forgot_password/{username}",response_model= schemas.Account)
def forgot_password(username:str,db: database.Session= Depends(database.get_db)):
    db_account = account.get_account(db, username= username)
    if not db_account:
        raise HTTPException(status_code=400, detail="This account does not exist")
    
    letters = string.ascii_letters
    new_password =  ''.join(random.choice(letters) for i in range(10))
    account.change_account_password(db,username=username,password=new_password)

    content="""\
    <html>
    <body>
        <p>Hi,<br>
        Your new password below, please keep it secret <br>
        <span style="color:red; font-size:30px;"> {} </span> <br>
        Best regards
        </p>
    </body>
    </html>
    """.format(new_password)
    my_email.send_email(username,"Re-send password",content)
    return db_account