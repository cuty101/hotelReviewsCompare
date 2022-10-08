#This will not run on online IDE
import requests
import csv
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options 




def gethotelsdotcom(hotelcount,morereviewcount):
    with open("reviews.csv","a+",encoding='utf-8') as file_writer:
        fields=["Hotel Name","Content","Rating","Date of stay"]
        writer=csv.DictWriter(file_writer,fieldnames=fields)
        writer.writeheader()

    with open("hotels.csv","a+",encoding='utf-8') as file_writer2:
        fields2=["Hotel Name","Hotel Rating","price","Number of Reviews","Cleanliness","Service"]
        writer2=csv.DictWriter(file_writer2,fieldnames=fields2)
        writer2.writeheader()
    URL = "https://sg.hotels.com/Hotel-Search?adults=2&d1=2022-10-04&d2=2022-10-05&destination=Singapore%2C%20Singapore&endDate=2022-10-05&latLong=1.29027%2C103.85201&regionId=3168&selected=&semdtl=&sort=RECOMMENDED&startDate=2022-10-04&theme=&useRewards=false&userIntent="
    r = requests.get(URL)
    driver = webdriver.Chrome("C:\\Users\\Ethan\\Downloads\\chromedriver_win32\\chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")
    soup = BeautifulSoup(r.content, 'html.parser') # If this line causes an error, run 'pip install html5lib' or install html5lib
    hotels = soup.find_all('li', class_ = 'uitk-spacing uitk-spacing-margin-blockstart-three')
    print(len(hotels))
    hotelslist = []
    hotel_num = 0
    desired_hotels = hotelcount
    while hotel_num < desired_hotels:
        try:
            hotel_element = {}
            header = hotels[hotel_num].find_all('h3',class_ = 'uitk-heading uitk-heading-6 is-visually-hidden')
            hotelname = header[0].contents[0]
            reviewsclass = hotels[hotel_num].find_all('span',class_ = 'is-visually-hidden')
            reviews = reviewsclass[0].contents[0]
            priceclass = hotels[hotel_num].find_all('div',class_ = 'uitk-text uitk-type-600 uitk-type-bold uitk-text-emphasis-theme')
            price = priceclass[0].contents[0].strip("S$")
            innerpagelink = "http://sg.hotels.com" + hotels[hotel_num].find_all('a', class_ = 'uitk-card-link')[0]["href"]
            hotel_element['Hotel Name'] = hotelname
            hotel_element['price'] = price


            #go to the hotel page itself
            driver.get(innerpagelink)
            hotelpagehtml = driver.page_source
            hotelsoup = BeautifulSoup(hotelpagehtml, 'html.parser')
            hotel_element['Hotel Rating'] = hotelsoup.find_all('h3',class_ = 'uitk-heading uitk-heading-5 uitk-spacing uitk-spacing-padding-blockend-three')[0].contents[0].split('/')[0]
            hotel_element['Number of Reviews'] = hotelsoup.find_all('button',class_ = 'uitk-link uitk-spacing uitk-spacing-padding-blockstart-two uitk-link-align-left uitk-link-layout-default uitk-link-medium')[0].contents[0].strip("See all ").strip(" reviews")
            if int(hotel_element['Number of Reviews'].replace(",","")) < 300:
                print(f"Skipping {hotelname} for too few reviews ({str(hotel_element['Number of Reviews'])})")
                hotel_num += 1
                desired_hotels += 1
            else:
                time.sleep(2.5)
                #click show reviews
                button = driver.find_element(By.XPATH, "//button[contains(@class, 'uitk-link uitk-spacing uitk-spacing-padding-blockstart-two uitk-link-align-left uitk-link-layout-default uitk-link-medium')]")
                button.click()
                time.sleep(2.5)
                for x in range(morereviewcount):
                    try:
                        #keep clicking more reviews
                        showmorebutton = driver.find_element(By.XPATH, "//button[text()='More reviews']")
                        showmorebutton.click()
                        time.sleep(1)
                    except:
                        break
                innerpagehtml = driver.page_source
                #scrape reviews
                innersoup = BeautifulSoup(innerpagehtml, 'html.parser')
                #attrs
                attrs = innersoup.find_all('div',class_ = 'uitk-layout-flex-item-align-self-flex-end uitk-layout-flex-item uitk-progress-bar-value')
                hotel_element["Cleanliness"] = attrs[0].contents[0].split('/')[0]
                hotel_element["Service"] = attrs[1].contents[0].split('/')[0]
                reviews = innersoup.find_all('div', class_ = 'uitk-card-content-section uitk-card-content-section-border-block-end uitk-card-content-section-padded')
                print(len(reviews))
                # print(hotels[0].prettify())
                reviewslist = []
                for review_num in range(len(reviews)):
                    review = {}
                    #print(reviews[review_num])
                    
                    try:
                        try:
                            review['Content'] = reviews[review_num].find_all("span", itemprop="description")[0].contents[0]
                        except:
                            review['Content'] = "N/A"
                        review['Date of stay'] = reviews[review_num].find_all("span", itemprop="datePublished")[0].contents[0]
                        review['Rating'] = reviews[review_num].find_all("span", itemprop="ratingValue")[0].contents[0].split("/")[0]
                        review["Hotel Name"] = hotelname
                        reviewslist.append(review)
                    except Exception as e: 
                        print(e)
                        print(reviews[review_num])
                        input("")
                        
                with open("reviews.csv","a+",encoding='utf-8') as file_writer:

                    fields=["Hotel Name","Content","Rating","Date of stay"]

                    writer=csv.DictWriter(file_writer,fieldnames=fields)

                    for x in reviewslist:
                        try:
                            writer.writerow(x)   
                        except:
                            continue
                with open("hotels.csv","a+",encoding='utf-8') as file_writer2:
                    fields2=["Hotel Name","Hotel Rating","price","Number of Reviews","Cleanliness","Service"]
                    writer2=csv.DictWriter(file_writer2,fieldnames=fields2)

                    writer2.writerow(hotel_element)   

                
                print(f"{str(hotel_num+1)}. {hotelname} scraped")
                hotel_num += 1
        except:
            hotel_num += 1
            desired_hotels += 1
        #print(innersoup)

    
    return

gethotelsdotcom(20,29)
