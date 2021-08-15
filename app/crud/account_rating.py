from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.sql.functions import mode
import models, schemas

def get_account_rating(db: Session, username: str):
    return db.query(models.Account_rating).filter(models.Account_rating.nguoibidanhgia == username).all()

def get_account_rating_detail(db:Session, who:str, towhom:str, time: datetime):
    account_rating_detail = db.query(models.Account_rating).filter(models.Account_rating.nguoibidanhgia == towhom,models.Account_rating.nguoidanhgia == who,models.Account_rating.time == time).first()
    return account_rating_detail

def create_account_rating(db: Session, account_rating: schemas.Account_rating_Create):
    now = datetime.now()
    db_account_rating = models.Account_rating(**account_rating.dict())
    db_account_rating.time = now.strftime("%Y-%m-%d %H:%M:%S")
    db.add(db_account_rating)
    db.commit()
    db.refresh(db_account_rating)
    return db_account_rating

def delete_account_rating_detail(db:Session, who:str, towhom:str, time: datetime):
    account_rating_detail = db.query(models.Account_rating).filter(models.Account_rating.nguoibidanhgia == towhom,models.Account_rating.nguoidanhgia == who,models.Account_rating.time == time).first()
    db.delete(account_rating_detail)
    db.commit()

def edit_account_rating(db: Session, account_rating: schemas.Account_rating_time):
    account_rating_dict = dict(account_rating)
    account_rating_db = db.query(models.Account_rating).filter(models.Account_rating.nguoidanhgia == account_rating_dict['nguoidanhgia'],models.Account_rating.nguoibidanhgia == account_rating_dict['nguoibidanhgia'],models.Account_rating.time == account_rating_dict['time']).first()
    account_rating_db.content = account_rating_dict['content']
    account_rating_db.point = account_rating_dict['point']
    db.commit()
    db.refresh(account_rating_db)
    return account_rating_db

def hide_account_rating(db:Session, who:str, towhom:str, time: datetime):
    account_rating_detail = db.query(models.Account_rating).filter(models.Account_rating.nguoibidanhgia == towhom,models.Account_rating.nguoidanhgia == who,models.Account_rating.time == time).first()
    account_rating_detail.status = 0
    db.commit()
    return account_rating_detail