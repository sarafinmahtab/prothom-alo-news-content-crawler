import requests
from bs4 import BeautifulSoup

import re

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from save_data import *


def trade_spider(max_pages):
    page = 201
    while page <= max_pages:
        url = 'https://www.prothomalo.com/sports/article/?tags=95&page=' + str(page)
        source_code = requests.get(url, params=None)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, features="lxml")
        for link in soup.findAll('a', {'class': 'link_overlay'}):
            href = link.get('href')
            if "sports" not in href:
                continue
            get_single_page_comments(href, str(page))
        page += 1


def get_single_page_comments(item_url, page):
    found_item = re.search('/sports/article/(.+?)/', item_url)
    if found_item:
        content_id = found_item.group(1)
        response = requests.get('https://www.prothomalo.com/api/comments/get_comments_json/?content_id=' + content_id)
        json_data = response.json()

        nonword_pattern = re.compile('[.@_!#$%^&*()<>?/|}{~:DpP0123456789 ১২৩৪৫৬৭৮৯০]*$')

        for comment_id in json_data:
            comment_object = json_data[comment_id]
            comment = comment_object['comment']

            if not nonword_pattern.fullmatch(comment):

                if ' ' not in comment:
                    continue

                try:
                    lang = detect(comment)

                    if lang == "bn":
                        formatted_comment = '---------------------------------' \
                                            + '\nComment ID: ' + comment_id \
                                            + '\nContent ID: ' + content_id \
                                            + '\nPage no: ' + page \
                                            + '\n' + comment + '\n\n'
                        print(formatted_comment)
                        insert_data_to_file(project_name, formatted_comment)
                except LangDetectException:
                    pass


project_name = "prothom-alo"
create_project_dir(project_name)

trade_spider(253)

# Total Page : 253


# Cricket -> https://www.prothomalo.com/sports/article/?tags=95&page=253
# Asia Cup -> https://www.prothomalo.com/sports/article?tags=2662&page=13
