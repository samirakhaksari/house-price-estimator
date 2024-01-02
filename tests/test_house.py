import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import create_house, House, City, Base


class HouseTestCase(unittest.TestCase):
    def test_simple_create(self):
        s = "sqlite:///MaskanFee-test.sqlite"
        engine = create_engine(s)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db = Session()
        db.query(City).delete()
        db.query(House).delete()
        db.commit()
        create_house(db, 'مشهد', 'سجاد', 1390, 2000000000, 120, floor=1,title_deeds=1,elevator=1,parking=1,store_room=1,unit_per_floor=1,total_unit=1)
        cities = db.query(City).all()
        self.assertEqual(len(cities), 1)
        self.assertEqual(cities[0].name, 'مشهد')





if __name__ == '__main__':
    unittest.main()
