from fastapi import APIRouter,Depends,status,Response,HTTPException
from typing import List
import schemas,database
from crud import company_rating

router =  APIRouter(
    tags = ["Company_rating"], 
    prefix = "/company_rating"
)

@router.get("/{company_id}", response_model=schemas.Company_rating)
def read_account_rating(company_id: int, db: database.Session = Depends(database.get_db)):
    db_company_rating = company_rating.get_company_rating(db, company_id= company_id)
    if db_company_rating is None:
        raise HTTPException(status_code=404, detail="Empty")
    return db_company_rating