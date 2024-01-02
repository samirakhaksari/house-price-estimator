import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crawler import create_records_from_main_list_text
from models import House, City, Base


class CrawlerTestCase(unittest.TestCase):
    def test_crawl_2nabsh_from_list(self):
        with open('2nabsh-main-list.html', encoding='utf8') as f:
            main_list = f.read()

        s = "sqlite:///MaskanFee-test.sqlite"
        engine = create_engine(s)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        db = Session()
        db.query(City).delete()
        db.query(House).delete()
        db.commit()
        create_records_from_main_list_text(db, main_list)
        houses = db.query(House).all()
        self.assertEqual(len(houses), 20)
        self.assertEqual(houses[0].area, 160)
        self.assertEqual(houses[0].price, 960060)


if __name__ == '__main__':
    unittest.main()
