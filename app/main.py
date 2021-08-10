from fastapi import FastAPI
import models
from database import engine
from router import account,resume,authentication,company,job_post,job_mark_apply,account_rating,company_rating

app= FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(account.router)
app.include_router(resume.router)
app.include_router(company.router)
app.include_router(job_post.router)
app.include_router(job_mark_apply.router)
app.include_router(account_rating.router)
app.include_router(company_rating.router)