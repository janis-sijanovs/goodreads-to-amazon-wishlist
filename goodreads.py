# Get the Goodreads  to-read-list HTML
from bs4 import BeautifulSoup
from typing import List
import requests

from helpers import clean_string

def get_goodreads_book_list(list_ID: str) -> List[str]:
    """Returns a cleaned list of book titles from goodreads.com"""
    goodreads_session = requests.Session()
    goodreads_to_read_url = f"https://www.goodreads.com/review/list/{list_ID}?shelf=to-read"
    goodreads_response = goodreads_session.get(goodreads_to_read_url)
    goodreads_soup = BeautifulSoup(goodreads_response.text, "html.parser")

    # Extract book titles from Goodreads "To-Read" list
    book_titles = []
    book_elements = goodreads_soup.select(".title div.value a")
    for element in book_elements:
        book_titles.append(clean_string(element.text.strip()))

    return book_titles