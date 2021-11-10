from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from urllib.parse import quote_plus
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request
from selenium.webdriver.chrome.options import Options
import os




keywords = ["surprised_human_face","happy_human_face","sad_human_face","neutral_human_face","angry_human_face"]
imgdir = ["surprised","happy","sad","neutral","angry"]

for i in range(5):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(r"C:\Users\parkj\project4\image\chromedriver.exe", options=chrome_options)
    driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")
    elem = driver.find_element_by_name("q")
    elem.send_keys(keywords[i])
    elem.send_keys(Keys.RETURN)
 
    SCROLL_PAUSE_TIME = 1
 
    last_height = driver.execute_script("return document.body.scrollHeight")
 
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
 
        time.sleep(SCROLL_PAUSE_TIME)
 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
            except:
                break
        last_height = new_height
 
    images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
    count = 1
    for image in images:
        try: 
            image.click()
            time.sleep(1)
            imgUrl = driver.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img").get_attribute("src")
            urllib.request.urlretrieve(imgUrl, os.path.dirname(os.path.realpath(__file__)) +"\\" +imgdir[i] + "\\" + str(count) + ".jpg")
            count = count + 1
        except:
            pass
        if count > 500 :
            break
    print("done!!")        
    driver.close()




