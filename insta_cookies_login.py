from selenium import webdriver
from selenium.webdriver.common.by import By

from comments_from_post import get_comments_per_post
import time
import json
import sys
import os
from config import USERNAME, PASSWORD

LINKS = []
POSTS = {}

def timer(func):
    def wrapper(*arg,**kwargs):
        t1 = time.time()
        res = func(*arg,**kwargs)
        t2 = time.time()
        print(func.__name__,'took',(t2-t1),'seconds')
        return res
    return wrapper

@timer
def login(driver):
    driver.get("https://www.instagram.com/accounts/login/")
    print("> loading instagram.com")
    print("> waiting for the page to load (4 seconds)")
    time.sleep(4)

    ### Login + Cookies + Notifications + Safe Login
    print("> accepting cookies")
    cookies = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/button[1]")
    cookies.click()

    ## username
    print("> entering username and password")
    input_username = driver.find_element(By.NAME, "username")
    time.sleep(0.7)
    for letter in USERNAME:
        input_username.send_keys(letter)
        time.sleep(0.05)
    time.sleep(0.7)

    ## password
    input_password = driver.find_element(By.NAME, "password")

    for letter in PASSWORD:
        input_password.send_keys(letter)
        time.sleep(0.08)
    time.sleep(1)
    submit = driver.find_element(By.XPATH, '//button[@type="submit"]')
    submit.click()
    print("> loging in")
    print("> wait for the pages to load (8 seconds)")
    time.sleep(8)

@timer
def basic_setup(driver):
    safe_info_button = driver.find_element(By.XPATH, '//button[text()="Not Now"]')
    safe_info_button.click()
    print("> do not activate notifications data")
    print("> wait for the pages to load (8 seconds)")
    time.sleep(8)
    notification_button = driver.find_element(By.XPATH, '//button[text()="Not Now"]')
    notification_button.click()
    print("> do not save the login data")
    print("> wait for the pages to load (8 seconds)")
    time.sleep(8)
    ### Go to Sophie Scholl Page after login
    print("> load https://www.instagram.com/ichbinsophiescholl/ and wait 8 seconds")
    driver.get('https://www.instagram.com/ichbinsophiescholl/') 
    time.sleep(8)

@timer
def get_post_links(driver):
    print("> scroll through the feed to get all posts")
    last_height = driver.execute_script("return document.body.scrollHeight")
    links = []
    time.sleep(0.5)
    while True:
        links += [post.get_attribute('href') for post in driver.find_elements(By.XPATH, '//article/div/div/div/div/a')]
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
            break
        last_height = new_height
    distinct_links = []

    for link in links:
        if link not in distinct_links:
            distinct_links.append(link)

    with open('postlinks.json','w') as f:
        json.dump(distinct_links,f)

    return distinct_links


def main(debug=True):
    print("> executing Firefox")
    driver = webdriver.Firefox()

    driver.maximize_window()
    login(driver)
    basic_setup(driver)

    post_count = driver.find_element(By.XPATH,"//header/section//span/span")
    post_links = []
    if os.path.exists("./postlinks.json"):
        with open('./postlinks.json','r') as f:
            post_links = json.load(f)
    
    distinct_links = []
    if len(post_links) != int(post_count.text):
        distinct_links = get_post_links(driver)
    else:
        distinct_links = post_links

    for index ,link in enumerate(distinct_links):
        print(index,'/',len(distinct_links),'>',link)
        POSTS[link] = get_comments_per_post(driver=driver,post_URL=link)

    return driver

def test():
    print("> executing Firefox")
    driver = webdriver.Firefox()

    driver.maximize_window()
    login(driver)
    basic_setup(driver)

    post_count = driver.find_element(By.XPATH,"//header/section//span/span")
    post_links = []
    if os.path.exists("./postlinks.json"):
        with open('./postlinks.json','r') as f:
            post_links = json.load(f)
    
    distinct_links = []
    if len(post_links) != int(post_count.text):
        distinct_links = get_post_links(driver)
    else:
        distinct_links = post_links

    for index ,link in enumerate(distinct_links):
        print(index,'/',len(distinct_links),'>',link)
        POSTS[link] = get_comments_per_post(driver=driver,post_URL=link)

    return driver

if __name__ == "__main__":
    driver = main()
    with open('save.json',"w") as f:
        json.dump(POSTS,f)