from sqlite3 import Time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


def timer(func):
    def wrapper(*arg,**kwargs):
        t1 = time.time()
        res = func(*arg,**kwargs)
        t2 = time.time()
        print(func.__name__,"with page:",kwargs['post_URL'],'took',(t2-t1),'seconds')
    return wrapper

@timer
def get_comments_per_post(driver:webdriver,post_URL:str='https://www.instagram.com/p/CPQsVCvnV0m/'):
    try:
        driver.get(post_URL)
    except TimeoutException as e:
        print(e)
        return None

    try:
        image_element = driver.find_element(By.XPATH, '//article/div/div[1]//img')
        image_element.get_attribute('alt')
        image_element.get_attribute('src')
    except:
        pass

    #image_caption = driver.find_element(By.XPATH, '//article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]')
    #print(image_caption.text)
    try:
        show_more = driver.find_element(By.XPATH, '//article/div/div[2]/div/div[2]/div[1]/ul/li')
    except:
        show_more = False
    while show_more:    
        element_count = len(driver.find_elements(By.XPATH, '//article//ul//li'))
        show_more.click()
        time.sleep(1.5)
        if element_count == len(driver.find_elements(By.XPATH, '//article//ul//li')) or element_count+1 == len(driver.find_elements(By.XPATH, '//article//ul//li')):
            break
        try:
            show_more = driver.find_element(By.XPATH, '//article/div/div[2]/div/div[2]/div[1]/ul/li')
        except:
            break
    try:
        reply = driver.find_element(By.XPATH, '//span[contains(text(),"View replies")]')
    except:
        reply = False
    while reply:
        reply.click()
        time.sleep(0.5)
        try:
            reply = driver.find_element(By.XPATH, '//span[contains(text(),"View replies")]')
        except:
            break
    comments = []
    for comment in driver.find_elements(By.XPATH, '//article//ul//li'):
        try:
            username = comment.find_element_by_xpath('.//h3//span[not(contains(text(),"View reply"))]').text
            content = comment.find_element_by_xpath('./div/div/div/span').text
            # print('username:', username)
            # print('comment:', content)
            temp_comment = {}
            temp_comment["username"] = username
            temp_comment["comment"] = content
            try:
                likes = comment.find_element_by_xpath('.//button[contains(text(),"like")]').text[0]
                #print('likes:', likes)
            except:
                likes = 0
                #print('likes:', 0)
            temp_comment["likes"] = likes
            comments.append(temp_comment)
            #print('___')
        except:
            pass

    return comments
