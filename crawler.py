import re
import logging

from models import *
from twill.commands import *
from twill import browser
from bs4 import BeautifulSoup


logging.basicConfig(filename='crawler.log', encoding='utf8', level=logging.DEBUG)


class House2Nabsh:
    def __init__(self, title, price, item_values):
        title_parts = title.split('،')
        self.area = title_parts[0].replace('متر', '').strip()
        self.region = title_parts[1].strip()
        self.price = ''.join(re.findall('\d+', price))
        self.data = {}
        for item_value in item_values:
            if 'خوابه' in item_value:
                key = 'store_room'
                value = item_value.replace('خوابه', '').strip()
            elif 'طبقه' in item_value:
                key = 'floor'
                value = item_value.replace('طبقه', '').strip()
            elif 'آسانسور' in item_value:
                key = 'elevator'
                value = True
            elif 'سند' in item_value:
                key = 'title_deeds'
                value = item_value.replace('سند', '').strip()
            elif 'سال ساخت' in item_value:
                key = 'building_year'
                age = int(item_value.replace('سال ساخت', '').strip())
                value = datetime.now().year - age
            else:
                continue
            self.data[key] = value


def crawl_divar():
    url = 'https://divar.ir/s/mashhad/buy-apartment'
    scraped_data = []
    go(url)
    print(browser.result.text)
    soup = BeautifulSoup(browser.result.text)
    articles = soup.find_all('article')
    for article in articles:
        article_link = 'https://divar.ir' + article.parent.attrs['href']
        go(article_link)
        article_content = browser.result.text
        assert 'متراژ' in article_content


def crawl_2nabsh_by_separate_page():
    url = 'https://www.2nabsh.com/%D8%A7%D9%85%D9%84%D8%A7%DA%A9-%D9%85%D8%B4%D9%87%D8%AF/%D8%AE%D8%B1%DB%8C%D8%AF-%D9%81%D8%B1%D9%88%D8%B4-%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86?sort=boosted_at'
    go(url)
    list_content = BeautifulSoup(browser.result.text)
    images = list_content.find_all('figcaption')
    for image in images:
        link_tag = image.contents[0].contents[0]
        link = link_tag.attrs['href']
        go(link)


def create_records_from_main_list_text(db, list_text):
    list_content = BeautifulSoup(list_text)
    articles = list_content.find_all('figcaption')
    for article in articles:
        logging.warning('New house from 2nabsh' + article.text)
        title = article.contents[0].contents[0].contents[0].contents[1].text
        price = article.contents[0].contents[2].text
        item_values = []
        for item_value in article.contents[0].contents[1].contents:
            item_values.append(item_value.text)
        house_2nabsh = House2Nabsh(title, price, item_values)
        logging.debug('New house data extracted: %s', price)
        create_house(db, 'مشهد', house_2nabsh.region, price=house_2nabsh.price,
                     area=house_2nabsh.area, **house_2nabsh.data)


def get_2nabsh_main_list_text():
    url = 'https://www.2nabsh.com/%D8%A7%D9%85%D9%84%D8%A7%DA%A9-%D9%85%D8%B4%D9%87%D8%AF/%D8%AE%D8%B1%DB%8C%D8%AF-%D9%81%D8%B1%D9%88%D8%B4-%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86?sort=boosted_at'
    go(url)
    list_text = browser.result.text
    logging.debug(list_text)
    return list_text


def crawl_2nabsh_from_list():
    list_text = get_2nabsh_main_list_text()
    db = Session()
    try:
        create_records_from_main_list_text(db, list_text)
    finally:
        db.close()


if __name__ == '__main__':
    crawl_2nabsh_from_list()
