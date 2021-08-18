from fastapi import APIRouter,Depends,status,Response,HTTPException,Security
from router import oauth2
from typing import List
import schemas,database
from crud import company

router =  APIRouter(
    tags = ["Company"], 
    prefix = "/companies"
)

@router.get("", response_model=List[schemas.Company])
def read_conmpanys(skip: int = 0, limit: int = 100, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    companys = company.get_companys(db, skip=skip, limit=limit)
    return companys

@router.get("/{company_id}", response_model = schemas.Company)
def read_conmpanys_by_id( company_id: int,db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    companys = company.get_company(db=db,id= company_id)
    if companys is None:
        raise HTTPException(status_code=404, detail="Comapny not found")
    return companys

@router.post("",response_model=schemas.Company)
def create_company(compnaies: schemas.Company_Create, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    return company.create_company(db,compnaies)

@router.put( "/accept/{company_id}",status_code =200)
def accept_company(company_id: int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    company.accept_company(db=db,company_id= company_id)
    return {"Message":"Success"}

@router.put( "/disable/{company_id}",status_code =200)
def disable_company(company_id: int, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Security(oauth2.get_current_user, scopes=["1"])):
    company.disable_company(db=db,company_id= company_id)
    return {"Message":"Success"}

@router.put( "/update/{company_id}",response_model=schemas.Company)
def update_company(company_id: int,compnaies: schemas.Company_Create, db: database.Session = Depends(database.get_db),current_user: schemas.Account_Info = Depends(oauth2.get_current_user)):
    return company.update_company(db,compnaies,company_id=company_id)
