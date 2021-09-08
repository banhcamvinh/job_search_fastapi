from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import models
from database import engine
from router import account,resume,authentication,company,job_post,job_mark,account_rating,company_rating,job_apply


app= FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(),"Error":"Input invalid"}),
    )

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(account.router)
app.include_router(resume.router)
app.include_router(company.router)
app.include_router(job_post.router)
app.include_router(job_mark.router)
app.include_router(job_apply.router)
app.include_router(account_rating.router)
app.include_router(company_rating.router)
