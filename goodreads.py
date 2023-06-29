# Get the Goodreads  to-read-list HTML
from bs4 import BeautifulSoup
from typing import List
import requests

from helpers import clean_string

def get_goodreads_book_list(list_ID: str) -> List[str]:
    """Returns a cleaned list of book titles from goodreads.com"""
    goodreads_session = requests.Session()
    end_of_list = False
    page = 1

    while not end_of_list:
        goodreads_to_read_url = f"https://www.goodreads.com/review/list/{list_ID}?shelf=to-read?page={page}"
        goodreads_response = goodreads_session.get(goodreads_to_read_url)
        goodreads_soup = BeautifulSoup(goodreads_response.text, "html.parser")
        page += 1

        # Extract book titles from Goodreads "To-Read" list
        book_titles = []
        book_elements = goodreads_soup.select(".title div.value a")
        for element in book_elements:
            book_titles.append(clean_string(element.text.strip()))
        if not book_elements:
            end_of_list = True

    return book_titles