from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import models, schemas

def get_account_rating(db: Session, username: str):
    return db.query(models.Account_rating).filter(models.Account_rating.nguoibidanhgia == username).first()

# def create_job_post(db: Session, job_post: schemas.Job_post_Create, username: str, id_company: int):
#     db_job_post = models.Job_post(**job_post.dict(), posted_by=username,about_company= id_company)
#     db.add(db_job_post)
#     db.commit()
#     db.refresh(db_job_post)
#     return db_job_post
