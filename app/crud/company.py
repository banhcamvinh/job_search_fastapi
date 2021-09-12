from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import models, schemas
from fastapi import HTTPException

def get_company(db: Session, id: int):
    return db.query(models.Company).filter(models.Company.id == id).first()

def get_companys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()

def get_companys_inactive(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).filter(models.Company.status == 0).offset(skip).limit(limit).all()

def get_active_companys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).filter(models.Company.status != 0).offset(skip).limit(limit).all()

def get_companies_filter(filters:dict,db: Session, skip: int = 0, limit: int = 100):
    companies = db.query(models.Company)
    for attr,val in filters.items():
        companies= companies.filter(getattr(models.Company,attr).ilike('%{}%'.format(val))).filter(models.Company.status != 0)
    return companies.all()

def create_company(db: Session, company: schemas.Company_Create):
    db_company = models.Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def accept_company(db: Session, company_id: int):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if db_company != None:
        db_company.status = 1
        db.commit()
        db.refresh(db_company)
    else:
        raise HTTPException(status_code=404, detail="Comapny not found")
    return db_company

def disable_company(db: Session, company_id: int):
    db_company = db.query(models.Company).filter(models.Company.id == company_id, models.Company.status != 0).first()
    if db_company != None:
        db_company.status = 0
        db.commit()
        db.refresh(db_company)
    else:
        raise HTTPException(status_code=404, detail="Comapny not found")
    return db_company

def update_company(db:Session,company: schemas.Company_Create,company_id:int ):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if db_company != None:
        company_dic = dict(company)
        db.query(models.Company).filter(models.Company.id == company_id).update(company_dic)
        db.commit()
        db.refresh(db_company)
    else:
        raise HTTPException(status_code=404, detail="Comapny not found")
    return db_company