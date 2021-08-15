from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import models, schemas


def get_company_rating(db: Session, company_id: int):
    return db.query(models.Company_rating).filter(models.Company_rating.company_id == company_id).all()

def get_company_rating_detail(db:Session, username:str, company_id: int, time: datetime):
    company_rating_detail = db.query(models.Company_rating).filter(models.Company_rating.nguoidanhgia == username,models.Company_rating.company_id == company_id,models.Company_rating.time == time).first()
    return company_rating_detail

def create_company_rating(db: Session, company_rating: schemas.Company_rating_Create):
    now = datetime.now()
    db_company_rating = models.Company_rating(**company_rating.dict())
    db_company_rating.time = now.strftime("%Y-%m-%d %H:%M:%S")
    db.add(db_company_rating)
    db.commit()
    db.refresh(db_company_rating)
    return db_company_rating

def delete_company_rating_detail(db:Session, username:str, company_id:str, time: datetime):
    company_rating_detail = db.query(models.Company_rating).filter(models.Company_rating.nguoidanhgia == username,models.Company_rating.company_id == company_id,models.Company_rating.time == time).first()
    db.delete(company_rating_detail)
    db.commit()

def edit_company_rating(db: Session, company_rating: schemas.Company_rating_time):
    company_rating_dict = dict(company_rating)
    company_rating_db = db.query(models.Company_rating).filter(models.Company_rating.nguoidanhgia == company_rating_dict['nguoidanhgia'],models.Company_rating.company_id == company_rating_dict['company_id'],models.Company_rating.time == company_rating_dict['time']).first()
    company_rating_db.content = company_rating_dict['content']
    company_rating_db.point = company_rating_dict['point']
    db.commit()
    db.refresh(company_rating_db)
    return company_rating_db

def hide_company_rating(db:Session, username:str, company_id:str, time: datetime):
    company_rating_detail = db.query(models.Company_rating).filter(models.Company_rating.nguoidanhgia == username,models.Company_rating.company_id == company_id,models.Company_rating.time == time).first()
    company_rating_detail.status = 0
    db.commit()
    return company_rating_detail