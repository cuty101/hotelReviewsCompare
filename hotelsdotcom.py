#This will not run on online IDE
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options 

def gethotelsdotcom():
    URL = "https://sg.hotels.com/Hotel-Search?adults=2&d1=2022-10-04&d2=2022-10-05&destination=Singapore%2C%20Singapore&endDate=2022-10-05&latLong=1.29027%2C103.85201&regionId=3168&selected=&semdtl=&sort=RECOMMENDED&startDate=2022-10-04&theme=&useRewards=false&userIntent="
    r = requests.get(URL)
    driver = webdriver.Chrome("C:\\Users\\Ethan\\Downloads\\chromedriver_win32\\chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")
    soup = BeautifulSoup(r.content, 'html.parser') # If this line causes an error, run 'pip install html5lib' or install html5lib
    hotels = soup.find_all('li', class_ = 'uitk-spacing uitk-spacing-margin-blockstart-three')
    print(len(hotels))
    hotelslist = []
    for hotel_num in range(20):
        hotel_element = {}
        header = hotels[hotel_num].find_all('h3',class_ = 'uitk-heading uitk-heading-6 is-visually-hidden')
        hotelname = header[0].contents[0]
        reviewsclass = hotels[hotel_num].find_all('span',class_ = 'is-visually-hidden')
        reviews = reviewsclass[0].contents[0]
        priceclass = hotels[hotel_num].find_all('div',class_ = 'uitk-text uitk-type-600 uitk-type-bold uitk-text-emphasis-theme')
        price = priceclass[0].contents[0].strip("S$")
        stars = reviews.split(' ')[0]
        totalreviews = reviews.replace("(","").split(' ')[-2]
        innerpagelink = "http://sg.hotels.com" + hotels[hotel_num].find_all('a', class_ = 'uitk-card-link')[0]["href"]
        hotel_element['name'] = hotelname
        hotel_element['price'] = price
        hotel_element['stars'] = stars
        hotel_element['review_count'] = totalreviews

        #go to the hotel page itself
        driver.get(innerpagelink)
        time.sleep(2.5)
        #click show reviews
        button = driver.find_element(By.XPATH, "//button[contains(@class, 'uitk-link uitk-spacing uitk-spacing-padding-blockstart-two uitk-link-align-left uitk-link-layout-default uitk-link-medium')]")
        button.click()
        time.sleep(2.5)
        for x in range(2):
            try:
                #keep clicking more reviews
                showmorebutton = driver.find_element(By.XPATH, "//button[text()='More reviews']")
                showmorebutton.click()
                time.sleep(1.5)
            except:
                break
        innerpagehtml = driver.page_source
        #scrape reviews
        innersoup = BeautifulSoup(innerpagehtml, 'html.parser')
        reviews = innersoup.find_all('div', class_ = 'uitk-card-content-section uitk-card-content-section-border-block-end uitk-card-content-section-padded')
        # print(hotels[0].prettify())
        reviewslist = []
        for review_num in range(len(reviews)-2):
            review = {}
            #print(reviews[review_num])
            
            try:
                review['desc'] = reviews[review_num].find_all("span", itemprop="description")[0].contents
                review['date'] = reviews[review_num].find_all("span", itemprop="datePublished")[0].contents
                review['stars'] = reviews[review_num].find_all("span", itemprop="ratingValue")[0].contents
                reviewslist.append(review)
            except:
                continue

        hotel_element["reviews"] = reviewslist
            
        #print(innersoup)
        hotelslist.append(hotel_element)


    return json.dumps(hotelslist)

with open("hotels.json","w+") as f:
    f.write(gethotelsdotcom())
