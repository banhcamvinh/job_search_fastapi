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

@router.post( "",response_model=schemas.Company)
def create_company(compnaies: schemas.Company_Create, db: database.Session = Depends(database.get_db)):
    return company.create_company(db,compnaies)


