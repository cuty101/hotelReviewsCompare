#imports
import csv
import json
import re
import time
from os.path import exists

import requests
from bs4 import BeautifulSoup as soup


#get soup
def getSoup(url):
    print(f"Trying to connect to {url}...")
    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
    bsobj = soup(html.content, 'lxml')
    print(f"{url} returned code {html.status_code}")
    time.sleep(10)
    return bsobj

#retrieve href of the next button
def goNextHotelPage(bsobj):
    print("Going to next page to fetch more hotels...")
    next = bsobj.find("a", {"class":"nav next ui_button primary"}).get("onclick").split(",")[-1]
    next = next.replace(" '", "")
    next = next.replace(");", "").lstrip()
    next = "https://www.tripadvisor.com"+next
    return next

#retrieve href of next button in reviews page
def goNextReviewPage(bsobj):
    print("Going to next page to fetch more reviews...")
    next = bsobj.find("a", {"class":"ui_button nav next primary"}).get("href")
    next = "https://www.tripadvisor.com"+next
    return next

#recursive function to retrieve the href of all hotel links in browsing page
def getHotelLink(bsobj, count):
    print("Getting the hotel links...")
    global hotelLink
    for name in bsobj.findAll('div', {"class":"listing_title"}):
        hotelhref = name.find("a", href=True).get("href")
        name = name.text.strip()
        print(f"Got link for {name}!")
        if not name.find("Sponsored"):                              #skips the junk(sponsored hotels) objects
            continue 
        else:
            name = re.sub("\d+\.\s", "", name)                      #removes the rank number from the hotel name
            hotelLink.append(hotelhref)
        count -= 1
        if count==0: return                                         #returns to main code after getting all hotel links
    bsobj = getSoup(goNextHotelPage(bsobj))
    getHotelLink(bsobj, count)                                      #function calls itself

#bubble rating, returns in an /10 scale
def bubbleRating(i):
    reviewRating = i.find("div", {"class":"Hlmiy F1"})
    if i.find("span", {"class":"ui_bubble_rating bubble_50"}): return 10
    elif i.find("span", {"class":"ui_bubble_rating bubble_45"}): return 9
    elif i.find("span", {"class":"ui_bubble_rating bubble_40"}): return 8
    elif i.find("span", {"class":"ui_bubble_rating bubble_35"}): return 7
    elif i.find("span", {"class":"ui_bubble_rating bubble_30"}): return 6
    elif i.find("span", {"class":"ui_bubble_rating bubble_25"}): return 5
    elif i.find("span", {"class":"ui_bubble_rating bubble_20"}): return 4
    elif i.find("span", {"class":"ui_bubble_rating bubble_15"}): return 3
    elif i.find("span", {"class":"ui_bubble_rating bubble_10"}): return 2

#retrieve the hotel data, Hotel Name, Rating, Total Reviews, Cleanliness, Service, Location ratings
def getHotelData(bsobj):
    scoreList = []
    hotelName = bsobj.find("h1", {"class":{"QdLfr b d Pn"}}).text               #hotelname
    reviewCount = bsobj.find("span", {"class":"qqniT"}).text.split().pop(0)     #review count
    pat = re.compile("([a-zA-z]+)(\d.\d)")
    score = bsobj.find_all("div", {"class":"WdWxQ"})
    hotelRating = float(bsobj.find("span", {"class":"uwJeR P"}).text)*2         #average rating of hotel in /10 rating scale
    hotelData = [hotelName, reviewCount, hotelRating]
    print(f"Getting {hotelName}'s data...")
    for i in score:
        temp = i.text
        scoreList.append(pat.match(temp).groups())
    del scoreList[-1]
    for i in range(len(scoreList)):
        temp = list(scoreList[i]).pop(1)
        hotelData.append(temp)                                                  #cleanliness, service, location ratings
    print(f"Got {hotelName}'s data!")
    return hotelData
    
#get all reviews from a review page and goes next page if not done
def getReviews(bsobj, count, reviewLinker):
    while reviewLinker > 9:
        bsobj = getSoup(goNextReviewPage(bsobj))
        reviewLinker -= 10
        count -= 10
    hotelName = bsobj.find("h1", {"class":{"QdLfr b d Pn"}}).text                   #hotel name
    reviewContent = bsobj.find_all("div", {"class":"YibKl MC R2 Gi z Z BB pBbQr"})  #review content
    for i in range(reviewLinker): 
        del reviewContent[0]
        count -= 1
    reviewLinker = 0
    hotelRating = bsobj.find("span", {"class":"uwJeR P"}).text                      #hotel rating
    print(f"Getting {hotelName}'s reviews...")
    for i in reviewContent:                                                         #recursive function to yield reviews 1 by 1
        reviewTitle = i.find("div", {"class":"KgQgP MC _S b S6 H5 _a"}).text        #review title
        reviewBody = i.find("div", {"class":"fIrGe _T"}).text                       #review content
        reviewRating = bubbleRating(i)                                              #review rating
        dateOfStay = i.find("span", {"class":"teHYY _R Me S4 H3"}).text.split(" ")
        dateOfStay = dateOfStay.pop(-2)+" "+dateOfStay.pop(-1)                      #date of stay
        reviewFull = [hotelName, reviewTitle, reviewBody, reviewRating, dateOfStay]
        yield reviewFull                                                            #return in a list
        count -= 1
        if count == 0: break
    print(f"Got {hotelName}'s reviews!")
    if count != 0:
        bsobj = getSoup(goNextReviewPage(bsobj))
        yield from getReviews(bsobj, count, reviewLinker)                           #function calls itself

#checks if filename laredy exists
def ifExists(f1, f2):
    if exists(f1):
        if exists(f2):
            return True

#removes linker and returns the linker value upon finding it
def removeLinker(fname):
    f = open(fname, "r+")
    lines=f.readlines()
    lines.pop()
    linker = lines.pop()
    lines.pop()
    lines.pop()
    f = open(fname, "w+")
    f.writelines(lines)
    f.close()
    return linker

#maincode
if __name__ == "__main__":
    global hotelLink
    bsobj = getSoup("https://www.tripadvisor.com/Hotels-g294265-Singapore-Hotels.html") #get soup
    hotelLink = []

    #Asks for user input
    try:
        tmp = int(input("How many hotels do you want?: "))
        tmp1 = int(input("How many reviews do you want per hotel?"))
    except:
        print("Are you stupid? Put a number.")
        exit()
    getHotelLink(bsobj, tmp)
    fname0 = input("What filename do you want your hotel data to be? (a csv file will be created): ")
    fname1 = input("What filename do you want your hotel reviews to be? (a csv file will be created): ")

    #initialization and checks if file exists and looks for linker if exists
    hotelHeader = ["Hotel Name", "Number of Reviews", "Hotel Rating", "Location", "Cleaniness", "Service"]
    reviewHeader = ["Hotel Name", "Title", "Content", "Rating", "Date of stay"]
    fname0 = fname0+".csv"
    fname1 = fname1+".csv"
    if ifExists(fname0, fname1):                                                                            #checks if file exists
        print(f"Found existing files {fname0} and {fname1}! Continuing from where you last left off...")    
        linker = int(removeLinker(fname0))                                                                  #finds for the linker. 
        for i in range(linker//tmp1): del hotelLink[0]                                                      #A linker is a number to track how many reviews has been retrieved, 
        reviewLinker = linker%tmp1                                                                          #and continues to ensure user has no need to restart scraping.
    else:
        print(f"Creating {fname0} and {fname1}...")
        linker = 0
        reviewLinker = 0
    f0 = open(fname0, "a+", encoding="utf-8")
    writer0 = csv.writer(f0)
    f1 = open(fname1, "a+", encoding="utf-8")
    writer1 = csv.writer(f1)

    #begin scraping...
    if linker == 0:
        print("Done!")
        writer0.writerow(hotelHeader)
        writer1.writerow(reviewHeader)
    try:
        for i in hotelLink:
            bsobj = getSoup("https://www.tripadvisor.com"+i)
            writer0.writerow(getHotelData(bsobj))
            score = bsobj.find_all("div", {"class":"WdWxQ"})
            for i in getReviews(bsobj, tmp1, reviewLinker):
                writer1.writerow(i)
                linker += 1
        print("If you see this, be glad because everything went smoothly~! HEHE :DDDDDDD")
    except Exception as e:
        print("Something unexpected happened!")
        print(e)
        print(f"Last written review is for hotel: {linker//tmp1+1}, review {linker-((linker//tmp1)*tmp1)}")
        writer0.writerow([linker])
    finally:
        f0.close()
        print(f"{fname0}: File saved")
        f1.close()
        print(f"{fname1}: File saved")