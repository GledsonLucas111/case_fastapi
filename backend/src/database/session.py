from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql://postgres:postgres@localhost:5432/fastapi", echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_session():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()