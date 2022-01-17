from sqlite3 import Time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


# Fehlerbeispiel : https://www.instagram.com/p/CYv4DvoMjQG/

def timer(func):
    """ 
    Documentation : decorator function to time other funtions runtime
    """
    def wrapper(*arg,**kwargs):
        t1 = time.time()
        res = func(*arg,**kwargs)
        t2 = time.time()
        print(func.__name__,"with page:",kwargs['post_URL'],'took',(t2-t1),'seconds')
        return res
    return wrapper

@timer
def get_comments_per_post(driver:webdriver,post_URL:str='https://www.instagram.com/p/CPQsVCvnV0m/'):
    """
    Documentation : function to request all comments and replies on one post
    """
    try:
        driver.get(post_URL)
    except TimeoutException as e:
        print(">> TimeoutException")
        return None
    time.sleep(2)

    post = {}
    post['link'] = post_URL
    try:
        image_element = driver.find_element(By.XPATH, '//article/div/div[1]//img')
        image_element.get_attribute('alt')
        image_element.get_attribute('src')
        post['image_src'] = image_element.get_attribute('src')
        post['image_alt'] = image_element.get_attribute('alt')
    except:
        post['image_src'] = ''
        post['image_alt'] = ''
        pass

    try:     
        caption = driver.find_element(By.XPATH,'//article//ul/div/li/div/div/div[2]/span')
        post['caption'] = caption.text
    except:
        post['caption'] = ''
        pass

    try:
        like_count = driver.find_element(By.XPATH,'//article//section[2]/div/div/a/span')
        post['likes'] = like_count.text
    except:
        post['likes'] = ''
        pass

    try:
        show_more = driver.find_element(By.XPATH, '//article/div/div[2]/div/div[2]/div[1]/ul/li')
    except:
        show_more = False

    while show_more:    
        element_count = len(driver.find_elements(By.XPATH, '//article//ul//li'))
        try:
            show_more.click()
        except:
            continue
        
        time.sleep(3)
        
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
        try:
            reply.click()
        except:
            continue

        time.sleep(3)
        try:
            reply = driver.find_element(By.XPATH, '//span[contains(text(),"View replies")]')
        except:
            break

    comments = []
    for comment in driver.find_elements(By.XPATH, '//article//ul//li'):
        try:
            username = comment.find_element(By.XPATH,'.//h3//span[not(contains(text(),"View reply"))]').text
            content = comment.find_element(By.XPATH,'./div/div/div/span').text
            temp_comment = {}
            temp_comment["username"] = username
            temp_comment["comment"] = content
            try:
                likes = int(comment.find_element(By.XPATH,'.//button[contains(text(),"like")]').text[0])
            except:
                likes = 0
            temp_comment["likes"] = likes
            comments.append(temp_comment)
        except:
            pass
    post['comments'] = comments
    print('>>',len(comments),"Kommentar[e] extrahiert.")
    return post
