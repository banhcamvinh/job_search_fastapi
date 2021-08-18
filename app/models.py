from datetime import date
from typing import Counter
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from sqlalchemy.sql.sqltypes import DATE, DateTime
from sqlalchemy.sql.visitors import traverse_using
from database import Base


class Account(Base):
    __tablename__ = "account"
    username = Column(String, primary_key=True)
    role = Column(Integer, default= 0,nullable= False)
    password = Column(String,nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(Date)
    sex = Column(Boolean)
    address = Column(String)
    phone = Column(String)
    status = Column(Integer, default=0, nullable= False)

    resumes = relationship('Resume',back_populates="account_create")
    job_posts = relationship('Job_post',back_populates="account_post")

    account_job_mark = relationship("Job_mark",back_populates="account")
    account_company_rating = relationship("Company_rating",back_populates="nguoidanhgia_account")


class Resume(Base):
    __tablename__ = "resume"
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String)
    overview = Column(String)
    position = Column(String)
    salary = Column(String)
    experience= Column(String)
    fields = Column(String)
    location = Column(String)
    academic_level= Column(String)
    tags = Column(String)
    status = Column(Integer, nullable= False)
    file = Column(String)
    # FK
    create_by = Column(String, ForeignKey('account.username'))

    account_create = relationship("Account",back_populates="resumes")
    resume_job_apply = relationship("Job_apply",back_populates="resume")

class Company(Base):
    __tablename__="company"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)
    logo = Column(String)
    website = Column(String)
    phone = Column(String)
    address = Column(String)
    overview = Column(String)
    industry = Column(String)
    founded = Column(Integer)
    size = Column(Integer)
    status = Column(Integer, nullable=False,default= 0)

    job_posts = relationship('Job_post',back_populates="company_post")
    company_company_rating = relationship('Company_rating',back_populates="company_id_company")

class Job_post(Base):
    __tablename__= "job_post"
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String)
    position = Column(String)
    salary = Column(String)
    academic_level = Column(String)
    experience = Column(String)
    type = Column(String)
    description = Column(String)
    requirements = Column(String)
    benefit = Column(String)
    quantity = Column(Integer)
    location = Column(String)
    fields = Column(String)
    tags = Column(String)
    create_time = Column(Date)
    update_time = Column(Date)
    expired_time = Column(Date)
    submit_expired_time =Column(Date)
    view = Column(Integer,default=0)
    status = Column(Integer,default=0)
    mode = Column(Integer,default=0)
    # FK
    posted_by = Column(String, ForeignKey('account.username'))
    about_company = Column(Integer, ForeignKey('company.id'))

    account_post = relationship("Account",back_populates="job_posts")
    company_post = relationship("Company",back_populates="job_posts")

    job_post_job_mark = relationship("Job_mark",back_populates="job_post")
    job_post_job_apply = relationship("Job_apply",back_populates="job_post")
    

class Job_mark(Base):
    __tablename__ = "job_mark"

    id_job = Column(ForeignKey('job_post.id'),primary_key=True)
    by_account = Column(ForeignKey('account.username'),primary_key=True)
    time = Column(DateTime)
    status = Column(Integer)

    account = relationship("Account", back_populates="account_job_mark")
    job_post = relationship("Job_post", back_populates="job_post_job_mark")

class Job_apply(Base):
    __tablename__= "job_apply"

    id_job = Column(ForeignKey('job_post.id'),primary_key=True)
    id_resume = Column(ForeignKey('resume.id'),primary_key=True)
    time = Column(DateTime)
    refer_code = Column(String)
    status = Column(Integer,nullable=False,default=1)

    resume = relationship("Resume", back_populates="resume_job_apply")
    job_post = relationship("Job_post", back_populates="job_post_job_apply")

class Account_rating(Base):
    __tablename__ = "account_rating"

    nguoidanhgia= Column(ForeignKey('account.username'),primary_key=True)
    nguoibidanhgia= Column(ForeignKey('account.username'),primary_key=True)
    time = Column(DateTime,primary_key=True)

    content = Column(String)
    point = Column(Integer)
    status= Column(Integer,nullable=False,default=1)

    nguoidanhgia_account=relationship("Account",foreign_keys=[nguoidanhgia])
    nguoibidanhgia_account=relationship("Account",foreign_keys=[nguoibidanhgia])

class Company_rating(Base):
    __tablename__ = "company_rating"

    nguoidanhgia= Column(ForeignKey('account.username'),primary_key=True)
    company_id = Column(ForeignKey('company.id'),primary_key=True)
    time = Column(DateTime,primary_key=True)

    content= Column(String)
    point = Column(Integer)
    status = Column(Integer,nullable=False,default=1)

    nguoidanhgia_account= relationship("Account", back_populates="account_company_rating")
    company_id_company= relationship("Company", back_populates="company_company_rating")

