import datetime
from sqlalchemy import orm
from sqlalchemy.sql.expression import update
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time,datetime


class Job_post_Base(BaseModel):
    title: str
    position: str
    salary: str
    academic_level: str
    experience: str
    type: str
    description: str
    requirements: str
    benefit: str
    quantity: int
    location: str
    fields: str
    tags: str

    submit_expired_time: date

class Job_post_db(Job_post_Base):
    status: Optional[int] = None
    mode: Optional[int] = None
    expired_time: Optional[date] = None
    create_time: Optional[date] = None
    update_time: Optional[date] = None

class Job_post_Create(Job_post_Base):
    pass

class Job_post(Job_post_Base):
    id: int
    posted_by: str
    about_company: int
    view: int
    class Config:
        orm_mode = True


class Resume_Base(BaseModel):
    title: str
    overview: str
    position: str
    salary: int
    experience: str
    fields: str
    location: str
    academic_level: str
    tags: str
    file: str

class Resume_Create(Resume_Base):
    pass

class Resume_db(Resume_Base):
    status: int

class Resume(Resume_Base):
    id: int
    create_by: str
    class Config:
        orm_mode = True

class Resume_Admin(Resume):
    status:int


class Account_Info_user(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
    sex: Optional[bool] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class Account_Base(BaseModel):
    username: str = "@gmail.com"
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
    sex: Optional[bool] = None
    address: Optional[str] = None
    phone: Optional[str] = None

class Account_db(Account_Base):
    status: int = 0
    role: int = 0

class Account_create(Account_Base):
    password: str

class Account_Admin(Account_Info_user):
    status: int = 0
    role: int = 0
    password: str
    class Config():
        orm_mode = True

class Account_password(BaseModel):
    password: str

class Account_Relationship(Account_Base):
    resumes: List[Resume] = []
    job_posts: List[Job_post] = []
    class Config():
        orm_mode = True

class Account_Info(Account_Base):
    class Config():
        orm_mode = True

class Account_db_orm(Account_db):
    class Config():
        orm_mode = True


class Company_Base(BaseModel):
    name: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    overview: Optional[str] = None
    industry: Optional[str] = None
    founded: Optional[int] = None
    size: Optional[int] = None

class Company_db(Company_Base):
    status: Optional[int] = None

class Company_Create(Company_Base):
    pass

class Company(Company_Base):
    id: int
    job_posts: List[Job_post] = []
    class Config():
        orm_mode = True


class Job_mark_Base(BaseModel):
    id_job: Optional[int] = None
    by_account: Optional[str] = None

class Job_mark_Create(Job_mark_Base):
    pass

class Job_mark_db(Job_mark_Base):
    time: Optional[datetime] = None
    status: Optional[int] = None

class Job_mark(Job_mark_Base):
    class Config():
        orm_mode = True


class Job_apply_Base(BaseModel):
    id_job: int
    id_resume: int
    refer_code: str

class Job_apply_Create(Job_apply_Base):
    pass

class Job_apply_db(Job_apply_Base):
    time: Optional[datetime] = None
    status: Optional[int] = None

class Job_apply(Job_apply_Base):
    job_post: Job_post = None
    resume: Resume = None
    class Config():
        orm_mode = True



class Account_rating_Base(BaseModel):
    nguoidanhgia: str
    nguoibidanhgia: str
    content: str
    point: int

class Account_rating_Create(Account_rating_Base):
    pass

class Account_rating_time(Account_rating_Base):
    time: datetime

class Account_rating_db(Account_rating_Base):
    time: Optional[datetime] = None
    status: Optional[int] = None

class Account_rating(Account_rating_Base):
    class Config():
        orm_mode= True


class Company_rating_Base(BaseModel):
    nguoidanhgia: str
    company_id: int
    content: str
    point: int

class Company_rating_Create(Company_rating_Base):
    pass

class Company_rating_time(Company_rating_Base):
    time: datetime

class Company_rating_db(Company_rating_Base):
    time: Optional[datetime] = None
    status: Optional[int] = None


class Company_rating(Company_rating_Base):
    class Config():
        orm_mode= True



class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str]=[]