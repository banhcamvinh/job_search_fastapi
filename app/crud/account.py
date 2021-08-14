from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.sql.functions import mode
import models, schemas
from hasing import Hash


def get_account(db: Session, username: str):
    return db.query(models.Account).filter(models.Account.username == username).first()

def get_active_account(db:Session, username: str):
    return db.query(models.Account).filter(models.Account.username == username,models.Account.status != 0).first()

def verify_account(db: Session, username:str):
    account = db.query(models.Account).filter(models.Account.username == username).first()
    if account != None:
        account.status=1
        db.commit()
        db.refresh(account)
    return account

def change_account_password(db: Session, username:str, password:str):
    account = db.query(models.Account).filter(models.Account.username == username).filter(models.Account.status != 0).first()
    if account != None:
        hashed_password = Hash.get_password_hash(password)
        account.password= hashed_password
        db.commit()
        db.refresh(account)
    return account

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).order_by(models.Account.username.asc()).offset(skip).limit(limit).all()

def create_account(db: Session, account: schemas.Account_create):
    hashed_password = Hash.get_password_hash(account.password)
    account.password= hashed_password
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def update_user_account_info(db:Session,account: schemas.Account_Info_user,username:str):
    db_account = db.query(models.Account).filter(models.Account.username == username).first()
    if db_account != None:
        account_dic = dict(account)
        db.query(models.Account).filter(models.Account.username == username).update(account_dic)
        db.commit()
        db.refresh(db_account)
    return db_account

def update_account_role(db:Session,username:str,role:int):
    db_account = db.query(models.Account).filter(models.Account.username == username).first()
    if db_account != None:
        db_account.role=role
        db.commit()
        db.refresh(db_account)
    return db_account

def disable_account(db:Session,username:str):
    db_account = db.query(models.Account).filter(models.Account.username == username).first()
    if db_account != None:
        db_account.status=0
        db.commit()
