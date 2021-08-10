from sqlalchemy import log
from crud import account
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import List
import schemas,database
from hasing import Hash
from router import my_token

router= APIRouter(
    tags=["Authetication"],
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm= Depends(), db: database.Session = Depends(database.get_db)):
    # check exist account and password
    accounts = account.get_account(db=db,username=request.username)
    if not accounts:
        raise HTTPException(status_code=404,detail=f"Account with {request.username} not found!")
    if not Hash.verify(accounts.password,request.password):
        raise HTTPException(status_code=404,detail= "Incorrect password!")

    # create access_token
    access_token = my_token.create_access_token(data={"sub": request.username,"scopes":str(accounts.role)})
    return {"access_token": access_token, "token_type": "bearer"}








# @router.post('/login')
# def login(login: schemas.Login, db: database.Session = Depends(database.get_db)):
#     accounts = account.get_account(db=db,username=login.username)
#     if not accounts:
#         raise HTTPException(status_code=404,detail=f"Account with {login.username} not found!")
#     if not Hash.verify(accounts.password,login.password):
#         raise HTTPException(status_code=404,detail= "Incorrect password!")

#     access_token = my_token.create_access_token(data={"sub": login.username})
#     return {"access_token": access_token, "token_type": "bearer"}