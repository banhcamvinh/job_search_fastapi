from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import models, schemas

def get_company(db: Session, id: int):
    return db.query(models.Company).filter(models.Company.id == id).first()

def get_companys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()

def create_company(db: Session, company: schemas.Company_Create):
    db_company = models.Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company