from sqlalchemy import orm
from sqlalchemy.sql.expression import update
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time


class Job_post_Base(BaseModel):
    title: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[str] = None
    academic_level: Optional[str] = None
    experience: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    benefit: Optional[str] = None
    quantity: Optional[int] = None
    location: Optional[str] = None
    fields: Optional[str] = None
    tags: Optional[str] = None
    create_time: Optional[date] = None
    update_time: Optional[date] = None
    expired_time: Optional[date] = None
    submit_expired_time: Optional[date] = None
    view: Optional[int] = None
    status: Optional[int] = None
    mode: Optional[int] = None

class Job_post_Create(Job_post_Base):
    pass

class Job_post(Job_post_Base):
    id: int
    posted_by: str
    about_company: int
    class Config:
        orm_mode = True


class Resume_Base(BaseModel):
    title: Optional[str] = None
    overview: Optional[str] = None
    position: Optional[str] = None
    salary: Optional[int] = None
    experience: Optional[str] = None
    fields: Optional[str] = None
    location: Optional[str] = None
    academic_level: Optional[str] = None
    tags: Optional[str] = None
    file: Optional[str] = None
    status: int

class Resume_Create(Resume_Base):
    pass

class Resume(Resume_Base):
    id: int
    create_by: str
    class Config:
        orm_mode = True


class Account_Base(BaseModel):
    username: str = "@gmail.com"
    role: int = 0
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
    sex: Optional[bool] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    status: int = 0

class Account_create(Account_Base):
    password: str = 123

class Account_password(BaseModel):
    password: str = 123

class Account(Account_Base):
    resumes: List[Resume] = []
    job_posts: List[Job_post] = []
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
    status: Optional[int] = None

class Company_Create(Company_Base):
    pass

class Company(Company_Base):
    id: int
    Job_posts: List[Job_post] = []
    class Config():
        orm_mode = True


class Job_mark_apply_Base(BaseModel):
    id_job: Optional[int] = None
    by_account: Optional[str] = None
    type: Optional[str] = None
    refer_code: Optional[str] = None
    time: Optional[date] = None
    status: Optional[int] = None

class Job_mark_apply_Create(Job_mark_apply_Base):
    pass

class Job_mark_apply(Job_mark_apply_Base):
    class Config():
        orm_mode = True


class Account_rating_Base(BaseModel):
    nguoidanhgia: Optional[str] = None
    nguoibidanhgia: Optional[str] = None
    time: Optional[date] = None
    content: Optional[str]= None
    point: Optional[int]= None
    status: Optional[int] = None

class Account_rating_Create(Account_rating_Base):
    pass

class Account_rating(Account_rating_Base):
    class Config():
        orm_mode= True


class Company_rating_Base(BaseModel):
    nguoidanhgia: Optional[str] = None
    company_id: Optional[int] = None
    time: Optional[date] = None
    content: Optional[str]= None
    point: Optional[int]= None
    status: Optional[int] = None

class Company_rating_Create(Company_rating_Base):
    pass

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