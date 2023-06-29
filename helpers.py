from selenium import webdriver
import re


def clean_string(input_string: str) -> str:
    """Removes \\n and multiple whitespaces"""
    # Remove \n from the string
    cleaned_string = input_string.replace('\n', '')
    
    # Remove extra whitespaces between words
    cleaned_string = re.sub(' +', ' ', cleaned_string)
    
    return cleaned_string


def headless_webdriver() -> webdriver.Chrome:
    """Returns a headless Chrome webdriver"""
    options = webdriver.ChromeOptions()
    # make sure the --verbose option is the first argument
    options.add_argument("--verbose")
    options.add_argument('--no-sandbox')
    # the chrome in linux only supports headless browser
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')

    return webdriver.Chrome(options=options)