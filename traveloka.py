import requests
from bs4 import BeautifulSoup
import nums_from_string
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

def countstars(starrow):
    fullstars = starrow.find_all('img',src = 'https://d1785e74lyxkqq.cloudfront.net/_next/static/v2/a/a7419e60fd1d8393884146a8f2732552.svg')
    halfstars = starrow.find_all('img',src = 'https://d1785e74lyxkqq.cloudfront.net/_next/static/v2/7/712367ee4e183cc414efbd8d338b4f49.svg')
    return len(fullstars)*2 + len(halfstars)

def traveloka():
    URL = "https://m.traveloka.com/en-sg/hotel/singapore/region/singapore-107493" #first page of hotel list
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome("C:\\Users\\xinying\\Downloads\\chromedriver.exe")

    hotels = soup.find_all("div", class_="tvat-hotelList") #its an array
    print("There are" , len(hotels) , " hotels in this page.")

    hotelslist = []



    for num in range(len(hotels)):
        hotel_objects = {} 
        
        hotelname = hotels[num].find_all("h3", class_="_20SY_ tvat-hotelName")[0].contents[0] #.content gives the name of hotels only
        hotelprice = hotels[num].find_all("span", class_="_2c6V9 tvat-hotelPrice")[0].contents[0].strip(" S$")
        star = hotels[num].find_all("div", class_="_1RoiH UZ77u tvat-starRating _1Fq-V")[0].contents[0]

        #to get number of stars
        stringstar = str(star)
        list_stringstar = [*stringstar]
        hotelstar = list_stringstar[15]

        #to get rating of hotel
        for i in hotels[num].find_all('div', attrs={'class':'_1Z-9g'}):
            rating = i.find('span', class_='tvat-ratingScore')
            stringrating = str(rating)
            list_stringrating = [*stringrating]
            rate = list_stringrating[31:34] #extract only the numerals for rating
            hotelrating = ""
            for x in rate:
                hotelrating += "" + x 

        #to get number of reviews
        for i in hotels[num].find_all('div', attrs={'class':'_1Z-9g'}):
            reviewC = i.find('span', class_='_227z0')
            stringreviewC = str(reviewC)
            hotelreviewcount = nums_from_string.get_nums(stringreviewC)[2] #nums_from_string is a library to extract numbers

        #to get each hotel link
        hotellinks = "https://m.traveloka.com/en-sg/hotel/singapore/region/singapore-107493" + hotels[num].find_all('a', class_ = '_16TPR')[0]["href"]

        hotel_objects['Name'] = hotelname
        hotel_objects['Price'] = hotelprice
        hotel_objects['Stars'] = hotelstar
        hotel_objects['Rating'] = hotelrating
        hotel_objects['Review Count'] = hotelreviewcount

        #automate to individual hotel pages
        driver.get(hotellinks)
        time.sleep(2)     #add delay in the execution of a program
        try:
            showmorebutton = driver.find_element(By.XPATH, "//div[text()='See All Reviews']")
            showmorebutton.click()
            print("Clicked button 1")
        except:
            driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
            time.sleep(1)
            showmorebutton = driver.find_element(By.XPATH, "//div[text()='Reviews']")
            showmorebutton.click()
            print("Button 1 failed, fallback to button 2")
        time.sleep(1)
        reviewshtml = driver.page_source
        reviewsoup = BeautifulSoup(reviewshtml,'html.parser')
        starsdiv = reviewsoup.find_all('div',class_ = "css-1dbjc4n r-vxcjpn r-bgc8nv")[1]
        starrow = starsdiv.find_all('div',class_ = 'css-1dbjc4n r-1awozwy r-18u37iz r-1h0z5md')
        cleanliness = countstars(starrow[0])
        service = countstars(starrow[4])
        print(f"Cleanliness: {str(cleanliness)}")
        print(f"Service: {str(service)}")
        review_list = []
        reviews = reviewsoup.find_all('div',class_='css-1dbjc4n r-1guathk r-1yzf0co')
        
        for x in range(len(reviews)):
            try:
                dateofstay = reviews[x].find_all('div',class_ = "css-901oao r-1ud240a r-1sixt3s r-1b43r93 r-b88u0q r-135wba7 r-fdjqy7 r-tsynxw")[0].contents[0]
                review_list.append({"Description":reviews[x].find_all('div',class_ = "css-901oao r-1sixt3s r-ubezar r-majxgm r-135wba7 r-fdjqy7")[0].contents[0],"Date of stay":dateofstay})
            except:
                continue


        #

        print(review_list)
        hotelslist.append(hotel_objects) 
        print(hotel_objects)

    #print(hotelslist)
    return hotelslist

traveloka()
