from sqlalchemy.sql import expression
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


@router.get("/me", response_model=schemas.Account_Info)
def read_account_for_user( db: database.Session = Depends(database.get_db), current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_account = account.get_account(db, username= current_user.username)
    if db_account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_account

@router.post("/me/change_password",response_model=schemas.Account_Info)
def change_account_password_for_user(accounts:schemas.Account_password, db: database.Session = Depends(database.get_db), current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_account =  account.change_account_password(db, username= current_user.username,password= accounts.password)
    if db_account is None:
        raise HTTPException(status_code=404, detail="User not found or disabled")
    return db_account

@router.get("/{username}", response_model=schemas.Account_db_orm)
def read_account_for_admin(username: str, db: database.Session = Depends(database.get_db), current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    db_account = account.get_account(db, username= username)
    if db_account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_account

@router.get( "",response_model=List[schemas.Account_Info])
def read_accounts_list_for_admin(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    accounts = account.get_accounts(db, skip=skip, limit=limit)
    return accounts

@router.post("/verify/{username}",response_model= schemas.Account_Info)
def verify_account(username: str, db: database.Session = Depends(database.get_db)):
    db_account= account.verify_account(db,username=username)
    if db_account is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_account

@router.post( "",response_model=schemas.Account_Info)
def create_account(accounts: schemas.Account_create, db: database.Session = Depends(database.get_db)):
    db_account = account.get_account(db, username= accounts.username)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    try:
        accounts = account.create_account(db,accounts)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong, please try again")

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
    try:
        my_email.send_email(accounts.username,"Verification Email for register our platform",content)
    except:
        account.del_account(db=db,username=accounts.username)
        raise HTTPException(status_code=400, detail="Sending email went wrong! Please try again")
    return accounts

@router.post("/forgot_password/{username}",response_model= schemas.Account_Info)
def forgot_password(username:str,db: database.Session= Depends(database.get_db)):
    db_account = account.get_active_account(db, username= username)
    if not db_account:
        raise HTTPException(status_code=400, detail="This account does not exist")
    
    old_pass = db_account.password
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
    try:
        my_email.send_email(username,"Re-send password",content)
    except:
        account.change_account_password(db,username=username,password=old_pass)
        raise HTTPException(status_code=400, detail="Sending email went wrong! Please try again")
    return db_account

@router.put("/me/update",response_model= schemas.Account_Info)
def update_user_account(accounts: schemas.Account_Info_user,db: database.Session= Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    db_account = account.get_active_account(db, username= current_user.username)
    if not db_account:
        raise HTTPException(status_code=400, detail="Account not exist or disabled")
    return account.update_user_account_info(db=db,account=accounts,username=current_user.username)

@router.put("/update/{username}",response_model= schemas.Account_Admin)
def update_user_account_for_admin(username:str, accounts: schemas.Account_Admin,db: database.Session= Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    db_account = account.get_active_account(db, username= username)
    if not db_account:
        raise HTTPException(status_code=400, detail="Account not exist or disabled")
    return account.update_user_account_info_by_admin(db=db,account=accounts,username= username)

@router.put("/role/{username}/{role}",response_model= schemas.Account_db_orm)
def update_account_role_for_admin(username:str,role:int,db: database.Session= Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    db_account = account.get_active_account(db, username= username)
    if not db_account:
        raise HTTPException(status_code=400, detail="Account not exist")

    content="""\
    <html>
    <body>
        <p>Hi,<br>
        Your account has been granted new permission <span style="color:red; font-size:30px;">{}</span><br>
        Best regards
        </p>
    </body>
    </html>
    """.format(role)
    my_email.send_email(username,"Your account has new permission",content)

    return account.update_account_role(db=db,username=username,role=role)

@router.put("/disable/{username}",status_code =200)
def disable_account_for_admin(username:str, db: database.Session=Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    db_account = account.get_active_account(db, username= username)
    if not db_account:
        raise HTTPException(status_code=400, detail="Account not exist")

    account.disable_account(db=db,username=username)

    content="""\
    <html>
    <body>
        <p>Hi,<br>
        Your account was deleted by admin on our platform<br>
        Best regards
        </p>
    </body>
    </html>
    """
    my_email.send_email(username,"Your account has been delete",content)

    return {"message":"success"}