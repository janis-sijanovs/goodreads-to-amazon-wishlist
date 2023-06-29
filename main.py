from selenium.common.exceptions import TimeoutException as SLTimeout
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium import webdriver

from goodreads import get_goodreads_book_list
from helpers import headless_webdriver
from dotenv import dotenv_values
from tqdm import tqdm
config = dotenv_values(".env")

book_titles = get_goodreads_book_list(config["GOODREADS_WISHLIST_ID"])

if not book_titles:
    print("No books in Goodreads found :(")
    print("Check the list ID")
    exit()

# Initialize Chrome webdriver
if config["RUN_HEADLESS"]:
    driver = headless_webdriver()
else:
    driver = webdriver.Chrome()

# Stealth driver just in case
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

# Navigate to the Amazon login page
driver.get('https://www.amazon.com')

# Sometimes amazon.com has a completely different UI
# Uncommenting this will check for the different layout

if config["CHECK_FOR_DIFFERENT_UI"]:
    try:
        el = WebDriverWait(driver, timeout=5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='nav-bb-right']//a[not(@class)]")))
        el.click()
    except SLTimeout:
        pass

try:
    el = WebDriverWait(driver, timeout=3).until(
        EC.element_to_be_clickable((By.ID, "nav-link-accountList")))
    el.click()
except SLTimeout:
    pass

if config["CHECK_FOR_DIFFERENT_UI"]:
    try:
        el = WebDriverWait(driver, timeout=3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "nav-action-signin-button")))
        el.click()
    except SLTimeout:
        pass

# Enter Email and Password

try:
    el = WebDriverWait(driver, timeout=30).until(
        EC.element_to_be_clickable((By.ID, "ap_email")))
    el.send_keys(config["AMAZON_EMAIL"])
except SLTimeout:
    print("Manual capcha required")
    print("or wrong Amazon UI loaded!")
    print("Try again!")
    exit()

el = driver.find_element(By.ID, "continue")
el.click()

try:
    el = WebDriverWait(driver, timeout=5).until(
        EC.element_to_be_clickable((By.ID, "ap_password")))
    el.send_keys(config["AMAZON_PASSWORD"])
except SLTimeout:
    print("Incorrect email :(")
    exit()

el = driver.find_element(By.ID, "signInSubmit")
el.click()

#######

list_exists = False

try:
    for i, book in enumerate(tqdm(book_titles)):

        # Search For The Book

        # Select the search bar
        try:
            el = WebDriverWait(driver, timeout=30).until(
            EC.element_to_be_clickable((By.ID, "twotabsearchtextbox")))
            
        except SLTimeout:
            if not i:
                print("Incorrect password / OTP required")
            else:
                print("Something went wrong when selecting the search bar")
            exit()

        # Clear the search bar and enter the book title
        el.clear()
        el.send_keys(book + " Book")

        # Press search
        el = driver.find_element(By.ID, "nav-search-submit-button")
        el.click()

        # Select the first search result

        try:
            el = WebDriverWait(driver, timeout=5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")))
        except SLTimeout:

            # If it doesn't exist, try pressing search again
            try:
                el = driver.find_element(By.ID, "nav-search-submit-button")
                el.click()

                el = WebDriverWait(driver, timeout=5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")))

            # If there's still no result, skip the book
            except SLTimeout:
                print(f'"{book}" not found :(')
                continue
        el.click()

        # Add to Wishlist

        try:
            el = WebDriverWait(driver, timeout=3).until(
            EC.element_to_be_clickable((By.ID, "add-to-wishlist-button-submit")))
            el.click()
        except SLTimeout:
            print(f'''"{book}" Couldn't be added to wishlist''')
            continue

        if not list_exists:
            try:
                # If there's no default list, make a new one
                el = WebDriverWait(driver, timeout=3).until(
                EC.element_to_be_clickable((By.ID, "list-name")))
                el.clear()
                el.send_keys("My GoodReads Book List")

                el = driver.find_element(By.ID, "wl-redesigned-create-list")
                el.click()

                try:
                    el = WebDriverWait(driver, timeout=3).until(
                    EC.element_to_be_clickable((By.ID, "a-autoid-35-announce")))
                    el.click()
                    print('New Wishlist "My GoodReads Book List" created!')
                except (SLTimeout):
                    pass

                list_exists = True
            
            except (SLTimeout):
                list_exists = True

        try:
            el = WebDriverWait(driver, timeout=3).until(
            EC.element_to_be_clickable((By.ID, "continue-shopping")))
            el.click()
        except (SLTimeout):
            pass
    
except:
    print(f"{i} out of {len(book_titles)} books added!")
    print(f'Failed on {i+1}. "{book}"')
else:
    print(f"{len(book_titles)} books successfully added! :O")