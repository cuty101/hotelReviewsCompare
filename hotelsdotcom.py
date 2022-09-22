import requests
from bs4 import BeautifulSoup
import json


def gethotelsdotcom():
    URL = "https://sg.hotels.com/Hotel-Search?adults=2&d1=2022-10-04&d2=2022-10-05&destination=Singapore%2C%20Singapore&endDate=2022-10-05&latLong=1.29027%2C103.85201&regionId=3168&selected=&semdtl=&sort=RECOMMENDED&startDate=2022-10-04&theme=&useRewards=false&userIntent="
    r = requests.get(URL)
    
    soup = BeautifulSoup(r.content, 'html.parser') # If this line causes an error, run 'pip install html5lib' or install html5lib
    hotels = soup.find_all('li', class_ = 'uitk-spacing uitk-spacing-margin-blockstart-three')
    print(len(hotels))
    # print(hotels[0].prettify())
    hotelslist = []
    for hotel_num in range(len(hotels)-1):
        hotel_element = {}
        header = hotels[hotel_num].find_all('h3',class_ = 'uitk-heading uitk-heading-6 is-visually-hidden')
        hotelname = header[0].contents[0]
        reviewsclass = hotels[hotel_num].find_all('span',class_ = 'is-visually-hidden')
        reviews = reviewsclass[0].contents[0]
        priceclass = hotels[hotel_num].find_all('div',class_ = 'uitk-text uitk-type-600 uitk-type-bold uitk-text-emphasis-theme')
        price = priceclass[0].contents[0].strip("S$")
        stars = reviews.split(' ')[0]
        totalreviews = reviews.replace("(","").split(' ')[-2]

        hotel_element['name'] = hotelname
        hotel_element['price'] = price
        hotel_element['stars'] = stars
        hotel_element['review_count'] = totalreviews
        hotelslist.append(hotel_element)

    return hotelslist
