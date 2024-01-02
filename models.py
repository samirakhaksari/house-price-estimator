import sqlalchemy as sa
from sqlalchemy import create_engine, Column, Integer, String, Date, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base
import csv
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

s = "sqlite:///maskan_fee.sqlite3"
engine = create_engine(s)
Session = sessionmaker(bind=engine)
Base = declarative_base()


log_filename = 'app.log'
max_log_size = 5 * 1024 * 1024
log_handler = RotatingFileHandler(log_filename, maxBytes=max_log_size, backupCount=3)
log_handler.setLevel(logging.INFO)

# Create a logger and add the handler
logger = logging.getLogger('')
logger.addHandler(log_handler)

# Set the log message format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)


class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(50))
    last_name = sa.Column(sa.String(50), nullable=False)
    phone = sa.Column(sa.String(50), nullable=False)
    email = sa.Column(sa.String(50), nullable=False)
    entry_date = sa.Column(sa.TIMESTAMP, server_default=sa.func.now())


class User_house(Base):
    __tablename__ = 'user_houses'
    id = sa.Column(sa.Integer, primary_key=True)
    house_type = sa.Column(sa.Enum('آپارتمان', 'ویلایی', 'زمین'))
    bargain_type = sa.Column(sa.String(50), nullable=True)
    city = sa.Column(sa.String(50), nullable=False)
    region = sa.Column(sa.String(50), nullable=False)
    area = sa.Column(sa.Integer, nullable=False)
    land_area = sa.Column(sa.Integer, nullable=True)
    Building_infrastructure = sa.Column(sa.Integer, nullable=False)
    building_year = sa.Column(sa.Integer, nullable=True)
    floor = sa.Column(sa.Integer, nullable=True)
    title_deeds = sa.Column(sa.String(50), nullable=True)
    elevator = sa.Column(sa.String(50), nullable=True)
    parking = sa.Column(sa.String(50), nullable=True)
    store_room = sa.Column(sa.String(50), nullable=True)
    balcony = sa.Column(sa.String(50), nullable=True)
    unit_per_floor = sa.Column(sa.String(50), nullable=True)
    total_unit = sa.Column(sa.String(50), nullable=True)
    price = sa.Column(sa.Integer, nullable=True)


class House(Base):
    __tablename__ = 'houses'
    id = sa.Column(sa.Integer, primary_key=True)
    house_type = sa.Column(sa.Enum('آپارتمان', 'ویلایی', 'زمین'))
    city_id = sa.Column(sa.Integer, sa.ForeignKey("cities.id"), nullable=True)
    region_id = sa.Column(sa.Integer, sa.ForeignKey("regions.id"), nullable=True)
    area = sa.Column(sa.Integer, nullable=True)
    land_area = sa.Column(sa.Integer, nullable=True)
    building_infrastructure = sa.Column(sa.Integer, nullable=True)
    building_year = sa.Column(sa.Integer, nullable=True)
    floor = sa.Column(sa.Integer, nullable=True)
    title_deeds = sa.Column(sa.String(50), nullable=True)
    elevator = sa.Column(sa.String(50), nullable=True)
    parking = sa.Column(sa.String(50), nullable=True)
    store_room = sa.Column(sa.String(50), nullable=True)
    balcony = sa.Column(sa.String(50), nullable=True)
    total_unit = sa.Column(sa.String(50), nullable=True)
    price = sa.Column(sa.Integer, nullable=True)
    create_date = sa.Column(sa.TIMESTAMP, server_default=sa.func.now())


class City(Base):
    __tablename__ = 'cities'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50))


class Region(Base):
    __tablename__ = 'regions'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100), nullable=False)
    city = sa.Column(sa.String(50))


class RegressionModel(Base):
    __tablename__ = 'regression_models'

    id = Column(Integer, primary_key=True)
    model_pickle = Column(LargeBinary)
    date = Column(Date, default=datetime.now)


def create_house(db, city, region, price, area, **kwavgs):
    city_record = db.query(City).filter(City.name == city).first()
    if city_record is None:
        city_record = City(name=city)
        db.add(city_record)
        db.commit()
        logger.info(f'Created a new city record: {city}')
    region_record = db.query(Region).filter(Region.name == region, Region.city == city).first()
    if region_record is None:
        region_record = Region(name=region, city=city)
        db.add(region_record)
        db.commit()
        logger.info(f'Created a new region record: {region} in city {city}')
    house = House(city_id=city_record.id, region_id=region_record.id, price=price, area=area,
                  **kwavgs)
    db.add(house)
    db.commit()
    db.close()
    logger.info(f'Created a new house record')


def export_csv():
    db = Session()
    file = open("houses.csv", "w", newline="")
    writer = csv.writer(file)
    columns = ['house.id', 'city_id', 'region_id', 'building_year', 'price', 'area']
    writer.writerow(columns)
    houses = db.query(House).filter(House.building_year.isnot(None)).all()
    for house in houses:
        writer.writerow([house.id, house.city_id, house.region_id, house.building_year, house.price, house.area])
    logger.info(f'Exported CSV file')

    file.close()


# Base.metadata.create_all(engine)

if __name__ == '__main__':
    # create_house(city='کهکیلویه و بویراحمد', region='سجاد', building_year=1390, price=2000000000, area=120)
    export_csv()
