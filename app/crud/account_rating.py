from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.sql.functions import mode
import models, schemas
from fastapi import HTTPException

def get_account_rating(db: Session, username: str):
    acc = db.query(models.Account).filter(models.Account.username == username).first()
    if acc is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(models.Account_rating).filter(models.Account_rating.nguoibidanhgia == username).all()

def get_account_rating_detail(db:Session, who:str, towhom:str, time: datetime):
    who_acc = db.query(models.Account).filter(models.Account.username == who).first()
    towhom_acc = db.query(models.Account).filter(models.Account.username == towhom).first()
    if who_acc is None:
        raise HTTPException(status_code=404, detail="Account used for rating not found")
    if towhom_acc is None:
        raise HTTPException(status_code=404, detail="Account is rated not found") 
    account_rating_detail = db.query(models.Account_rating).filter(models.Account_rating.nguoibidanhgia == towhom,models.Account_rating.nguoidanhgia == who,models.Account_rating.time == time).first()
    return account_rating_detail

def create_account_rating(db: Session, account_rating: schemas.Account_rating_Create):
    account_rating_dic = dict(account_rating)
    if account_rating_dic['point'] < 1 or account_rating_dic['point'] > 5:
        raise HTTPException(status_code=404, detail="Invalid point")
    who_acc = db.query(models.Account).filter(models.Account.username == account_rating_dic['nguoidanhgia']).first()
    towhom_acc = db.query(models.Account).filter(models.Account.username == account_rating_dic['nguoibidanhgia']).first()
    if who_acc is None:
        raise HTTPException(status_code=404, detail="Account used for rating not found")
    if towhom_acc is None:
        raise HTTPException(status_code=404, detail="Account is rated not found") 
    now = datetime.now()
    db_account_rating = models.Account_rating(**account_rating.dict())
    db_account_rating.time = now.strftime("%Y-%m-%d %H:%M:%S")
    db.add(db_account_rating)
    db.commit()
    db.refresh(db_account_rating)
    return db_account_rating

def delete_account_rating_detail(db:Session, who:str, towhom:str, time: datetime):
    who_acc = db.query(models.Account).filter(models.Account.username == who).first()
    towhom_acc = db.query(models.Account).filter(models.Account.username == towhom).first()
    if who_acc is None:
        raise HTTPException(status_code=404, detail="Account used for rating not found")
    if towhom_acc is None:
        raise HTTPException(status_code=404, detail="Account is rated not found") 
    account_rating_detail = db.query(models.Account_rating).filter(models.Account_rating.nguoibidanhgia == towhom,models.Account_rating.nguoidanhgia == who,models.Account_rating.time == time).first()
    if account_rating_detail != None:
        db.delete(account_rating_detail)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Account rating not found")


def edit_account_rating(db: Session, account_rating: schemas.Account_rating_time):
    account_rating_dict = dict(account_rating)
    if account_rating_dict['point'] < 1 or account_rating_dict['point'] > 5:
        raise HTTPException(status_code=404, detail="Invalid point")
    who_acc = db.query(models.Account).filter(models.Account.username == account_rating_dict['nguoidanhgia'], models.Account.status != 0).first()
    towhom_acc = db.query(models.Account).filter(models.Account.username == account_rating_dict['nguoibidanhgia'], models.Account.status != 0).first()
    if who_acc is None:
        raise HTTPException(status_code=404, detail="Account used for rating not found")
    if towhom_acc is None:
        raise HTTPException(status_code=404, detail="Account is rated not found") 
    account_rating_db = db.query(models.Account_rating).filter(models.Account_rating.nguoidanhgia == account_rating_dict['nguoidanhgia'],models.Account_rating.nguoibidanhgia == account_rating_dict['nguoibidanhgia'],models.Account_rating.time == account_rating_dict['time']).first()
    if account_rating_db is None:
        raise HTTPException(status_code=404, detail="account rating not found")
    account_rating_db.content = account_rating_dict['content']
    account_rating_db.point = account_rating_dict['point']
    now = datetime.now()
    account_rating_db.time = now.strftime("%Y-%m-%d %H:%M:%S")
    db.commit()
    db.refresh(account_rating_db)
    return account_rating_db

def hide_account_rating(db:Session, who:str, towhom:str, time: datetime):
    who_acc = db.query(models.Account).filter(models.Account.username == who).first()
    towhom_acc = db.query(models.Account).filter(models.Account.username == towhom).first()
    if who_acc is None:
        raise HTTPException(status_code=404, detail="Account used for rating not found")
    if towhom_acc is None:
        raise HTTPException(status_code=404, detail="Account is rated not found") 
    account_rating_detail = db.query(models.Account_rating).filter(models.Account_rating.nguoibidanhgia == towhom,models.Account_rating.nguoidanhgia == who,models.Account_rating.time == time).first()
    if account_rating_detail != None:
        account_rating_detail.status = 0
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Account rating not found")
    return account_rating_detail