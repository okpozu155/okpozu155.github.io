from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./visitor_count.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class VisitorCount(Base):
    __tablename__ = "visitor_count"
    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer, default=0)

# Create the database table
Base.metadata.create_all(bind=engine)

@app.get("/visitor-count")
def get_visitor_count():
    session = SessionLocal()
    visitor = session.query(VisitorCount).first()
    if not visitor:
        visitor = VisitorCount(count=1)
        session.add(visitor)
    else:
        visitor.count += 1
    session.commit()
    session.refresh(visitor)
    session.close()
    return {"count": visitor.count}
