from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import List
import schemas,database
from crud import company

router =  APIRouter(
    tags = ["Company"], 
    prefix = "/companies"
)

@router.get("", response_model=List[schemas.Company])
def read_conmpanys(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db)):
    companys = company.get_companys(db, skip=skip, limit=limit)
    return companys

@router.get("/{company_id}", response_model = schemas.Company)
def read_conmpanys_by_id( company_id: int,db: database.Session = Depends(database.get_db)):
    companys = company.get_company(db=db,id= company_id)
    return companys

@router.post("",response_model=schemas.Company)
def create_company(compnaies: schemas.Company_Create, db: database.Session = Depends(database.get_db)):
    return company.create_company(db,compnaies)

@router.put( "/accept/{company_id}",response_model=schemas.Company)
def accept_company(company_id: int, db: database.Session = Depends(database.get_db)):
    return company.accept_company(db=db,company_id= company_id)

@router.put( "/disable/{company_id}",response_model=schemas.Company)
def disable_company(company_id: int, db: database.Session = Depends(database.get_db)):
    return company.disable_company(db=db,company_id= company_id)

@router.put( "/update/{company_id}",response_model=schemas.Company)
def update_company(company_id: int,compnaies: schemas.Company_Create, db: database.Session = Depends(database.get_db)):
    return company.update_company(db,compnaies,company_id=company_id)
