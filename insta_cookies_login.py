from selenium import webdriver
from selenium.webdriver.common.by import By

from comments_from_post import get_comments_per_post
import time
import json

LINKS = []
POSTS = {}

def timer(func):
    def wrapper(*arg,**kwargs):
        t1 = time.time()
        res = func(*arg,**kwargs)
        t2 = time.time()
        print(func.__name__,'took',(t2-t1),'seconds')
    return wrapper

@timer
def main():
    
    driver = webdriver.Firefox()

    driver.maximize_window()

    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(4)
    USERNAME = "siggi_wahl"
    PASSWORD = "siggi_wahl_1234"

    ### Login + Cookies + Notifications + Safe Login
    cookies = driver.find_element(By.XPATH, "/html/body/div[4]/div/div/button[1]")
    cookies.click()

    ## username
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
    time.sleep(10)
    safe_info_button = driver.find_element(By.XPATH, '//button[text()="Not Now"]')
    safe_info_button.click()
    time.sleep(10)
    notification_button = driver.find_element(By.XPATH, '//button[text()="Not Now"]')
    notification_button.click() 
    time.sleep(5)
    ### Go to Sophie Scholl Page after login
    driver.get('https://www.instagram.com/ichbinsophiescholl/') 
    time.sleep(10)
    post = driver.find_element(By.XPATH, '//a[contains(@href,"/p/")]')

    last_height = driver.execute_script("return document.body.scrollHeight")
    posts = []
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

    links = list(set(links))
    LINKS = links
    for index ,link in enumerate(links):
        print(index,'/',len(links),'>',link)
        POSTS[link] = get_comments_per_post(driver=driver,post_URL=link)

if __name__ == "__main__":
    main()
    with open('save.json',"w") as f:
        json.dump(POSTS,f)