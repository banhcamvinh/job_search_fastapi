from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import models, schemas
from hasing import Hash

def get_account(db: Session, username: str):
    return db.query(models.Account).filter(models.Account.username == username).first()

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()

def create_account(db: Session, account: schemas.Account_create):
    hashed_password = Hash.get_password_hash(account.password)
    account.password= hashed_password
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account