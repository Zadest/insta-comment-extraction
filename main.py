from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# siggi_wahl
# siggi_wahl_1234

def main() -> webdriver:
    driver = webdriver.Firefox()
    driver.get("https://www.instagram.com/ichbinsophiescholl/")
    elements = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a")
    print(elements)
    time.sleep(10)
    return driver

if __name__ == "__main__":
    driver = main()