from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.sql.functions import mode
import models, schemas
from hasing import Hash


def get_account(db: Session, username: str):
    return db.query(models.Account).filter(models.Account.username == username).first()

def accept_account(db: Session, username:str):
    account = db.query(models.Account).filter(models.Account.username == username).first()
    if account != None:
        account.status=1
        db.commit()
        db.refresh(account)
    return account

def change_account_password(db: Session, username:str, password:str):
    account = db.query(models.Account).filter(models.Account.username == username).first()
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