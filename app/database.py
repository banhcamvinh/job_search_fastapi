from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session

# SQLALCHEMY_DATABASE_URL = "postgresql://gozkcjfjdzngrv:5395e2dd8c6a01418f07a66e6c182a093c37e2742beb5d7b7cc4c498464e282b@ec2-3-233-43-103.compute-1.amazonaws.com:5432/deo4s6sgprj7uo"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost:5432/jobwebsite"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db =  SessionLocal()
    try:
        yield db
    finally:
        db.close()
