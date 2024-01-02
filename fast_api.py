from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from models import Session

# Database setup using SQLAlchemy
DATABASE_URL = "sqlite:///house.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy Models
class House(Base):
    __tablename__ = "houses"
    id = Column(Integer, primary_key=True, index=True)
    house_type = Column(String, index=True)
    bargain_type = Column(String)
    city = Column(String)
    region = Column(String)
    area = Column(Integer)
    building_year = Column(Integer)
    floor = Column(Integer)
    title_deeds = Column(String)
    elevator = Column(Boolean)
    parking = Column(Boolean)
    store_room = Column(Boolean)
    price = Column(Integer)


Base.metadata.create_all(bind=engine)

app = FastAPI()


# Pydantic Model for House
class HouseCreate(BaseModel):
    house_type: str
    bargain_type: str
    city: str
    region: str
    area: int
    building_year: int
    floor: int
    title_deeds: str
    elevator: bool
    parking: bool
    store_room: bool
    price: int


class HouseResponse(BaseModel):
    id: int
    house_type: str
    bargain_type: str
    city: str
    region: str
    area: int
    building_year: int
    floor: int
    title_deeds: str
    elevator: bool
    parking: bool
    store_room: bool
    price: int


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new house
@app.post("/houses/", response_model=HouseResponse)
def create_house(house: HouseCreate, db: Session = Depends(get_db)):
    db_house = House(**house.dict())
    db.add(db_house)
    db.commit()
    db.refresh(db_house)
    return db_house


# Get a specific house by ID
@app.get("/houses/{house_id}", response_model=HouseResponse)
def read_house(house_id: int, db: Session = Depends(get_db)):
    db_house = db.query(House).filter(House.id == house_id).first()
    if db_house is None:
        raise HTTPException(status_code=404, detail="House not found")
    return db_house


# Update a specific house by ID
@app.put("/houses/{house_id}", response_model=HouseResponse)
def update_house(house_id: int, house: HouseCreate, db: Session = Depends(get_db)):
    db_house = db.query(House).filter(House.id == house_id).first()
    if db_house is None:
        raise HTTPException(status_code=404, detail="House not found")
    for key, value in house.dict().items():
        setattr(db_house, key, value)
    db.commit()
    db.refresh(db_house)
    return db_house


# Delete a specific house by ID
@app.delete("/houses/{house_id}", response_model=HouseResponse)
def delete_house(house_id: int, db: Session = Depends(get_db)):
    db_house = db.query(House).filter(House.id == house_id).first()
    if db_house is None:
        raise HTTPException(status_code=404, detail="House not found")
    db.delete(db_house)
    db.commit()
    return db_house
