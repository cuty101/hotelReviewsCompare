import collections
import functools
import operator
import string

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
from gensim.parsing.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nrclex import NRCLex
from wordcloud import WordCloud

porter_stemmer = PorterStemmer()

#get negative reviews for each hotel
def neg_reviews(overall_df):
    low_rating=[]
    ratings=overall_df['Rating']
    for rating in ratings:
        if rating<5:
            low_rating.append(rating)
    #get neg reviews
    negative_reviews_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    low_rating = set(low_rating)
    for i in low_rating:
        negative_reviews_df= pd.concat([negative_reviews_df,overall_df.loc[overall_df['Rating']==i]])
    negative_reviews_df.reset_index().drop(['index'], axis=1)
    
    return negative_reviews_df

#get positive reviews for each hotel
def pos_reviews(overall_df):
    high_rating=[]
    ratings=overall_df['Rating']
    for rating in ratings:
        if rating>=5:
            high_rating.append(rating)
    #get pos reviews
    positive_reviews_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    high_rating = set(high_rating)
    for i in high_rating:
        positive_reviews_df= pd.concat([positive_reviews_df,overall_df.loc[overall_df['Rating']==i]])
    
    return positive_reviews_df

#cleans the reviews by removing stopwords, punctuation and digits.
def clean_words(pos_df):
    all_words = [word.lower() for sent in pos_df['Content'] for word in word_tokenize(sent)]
    stop_words=set(stopwords.words("english"))
    all_words_clean=[]
    stopwords_list=set(stopwords.words('english'))
    stopwords_list.update(['hotel', 'would', 'us','get','come','back','nt','could','good','great','one','rooms'])
    for word in all_words:
        punc_free = ''.join([ch for ch in word if ch not in string.punctuation])
        if punc_free not in stopwords_list and not punc_free.isdigit():
            if len(punc_free)>=2:
                all_words_clean.append(punc_free)
    #get top 10 words 
    all_words_frequency=FreqDist(all_words_clean)
    top10=all_words_frequency.most_common(10)
    
    return top10
#prints graph that displays the top 10 words for positive reviews
def top_words_graph(top10):
    data = dict(top10)
    courses = (data.keys())
    values = (data.values())

    fig = plt.figure(figsize = (10, 5))

    # creating the bar plot
    plt.bar(courses, values, color ='blue',
            width = 0.4)

    plt.xlabel("Good reviews")
    plt.ylabel("Number of times mentioned")
    plt.title("Top words for reviews")
    plt.show()

#get reviews based on each top 10 words
def filtered_reviews_based_on_top10(top10, pos_df):
    top10_words=[]
    for i in top10:
        top10_words.append(i[0])
    list=[]
    for review in pos_df['Content']:
        for i in top10:
            if i[0] in review:
                list.append(review)
                break
    filtered_review = pd.DataFrame(list)
    return filtered_review

#separate reviews based on each top10 word into dataframes
def separate_reviews(filtered_review, top10):
    #get top 10 words out of tuple
    top10_words=[]
    for i in top10:
        top10_words.append(i[0])
   
    #separate reviews based on top10 words
    room_reviews=[]
    staff_reviews=[]
    stay_reviews=[]
    service_reviews=[]
    location_reviews=[]
    friendly_reviews=[]
    clean_reviews=[]
    nice_reviews=[]
    breakfast_reviews=[]
    food_reviews=[]
    for review in filtered_review[0]:
        for j in range(len(top10_words)):
            if j == 0:
                if top10_words[j] in review:
                    room_reviews.append(review)
            elif j == 1:
                if top10_words[j] in review:
                    staff_reviews.append(review)
            elif j == 2:
                if top10_words[j] in review:
                    stay_reviews.append(review)
            elif j == 3:
                if top10_words[j] in review:
                    service_reviews.append(review)
            elif j == 4:
                if top10_words[j] in review:
                    location_reviews.append(review)
            elif j == 5:
                if top10_words[j] in review:
                    friendly_reviews.append(review)
            elif j == 6:
                if top10_words[j]in review:
                    clean_reviews.append(review)
            elif j == 7:
                if top10_words[j]in review:
                    nice_reviews.append(review)
            elif j == 8:
                if top10_words[j]in review:
                    breakfast_reviews.append(review)
            elif j == 9:
                if top10_words[j]in review:
                    food_reviews.append(review)
                    
    #create dataframes                
    room_review = pd.DataFrame(room_reviews)
    staff_review = pd.DataFrame(staff_reviews)
    stay_review = pd.DataFrame(stay_reviews)
    service_review = pd.DataFrame(service_reviews)
    location_review = pd.DataFrame(location_reviews)
    friendly_review = pd.DataFrame(friendly_reviews)
    clean_review = pd.DataFrame(clean_reviews)
    nice_review = pd.DataFrame(nice_reviews)
    breakfast_review = pd.DataFrame(breakfast_reviews)
    food_review = pd.DataFrame(food_reviews)
 
    
    return room_review, staff_review, stay_review, service_review, location_review, friendly_review, clean_review, nice_review, breakfast_review, food_review

#convert list to dataframe for positive review
def convert_to_dataframe(review_list, pos_df):
    converted_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    for i in review_list[0]:
        converted_df= pd.concat([converted_df,pos_df.loc[pos_df['Content']==i]])
    converted_df.sort_values(by=['Hotel Name'])
    return converted_df

#concatenate all dataframes and sort by hotel name and the popular word
def concat_dataframes_get_unique_hotels(first_top_df, second_top_df,third_top_df,fourth_top_df,fifth_top_df,sixth_top_df,seventh_top_df,eighth_top_df,ninth_top_df,tenth_top_df):
    concatenated_dataframes = pd.concat([first_top_df, second_top_df,third_top_df,fourth_top_df,fifth_top_df,sixth_top_df,seventh_top_df,eighth_top_df,ninth_top_df,tenth_top_df])
    concatenated_dataframes=concatenated_dataframes.sort_values(by=['Hotel Name', 'Popular_Word'])
    concatenated_dataframes.rename(columns = {'Hotel Name':'Hotel_Name'}, inplace = True)
    
    return concatenated_dataframes

#get list of unique hotels
def unique_hotels_df(UniqueNames, UniqueHotel):
    list_of_df=[]
    for i in UniqueNames:
        df=UniqueHotel[i]
        df_unique= df[~df.index.duplicated(keep='first')]
        list_of_df.append(df_unique)
    return list_of_df

#prints out graph of reviewer's emotions. (Sentiment analysis)
def graph_for_reviewers_emotions(list_of_unique_hotel_df):
    emotion_for_each_hotel=[]
    for k in range(len(list_of_unique_hotel_df)):
        for i in list_of_unique_hotel_df[k]['Content']:
                emotion=NRCLex(i)
                emotions=emotion.raw_emotion_scores
                emotion_for_each_hotel.append(emotions)
    result = dict(functools.reduce(operator.add, map(collections.Counter, emotion_for_each_hotel)))
    data = result
    courses = (data.keys())
    values = (data.values())

    fig = plt.figure(figsize = (10, 5))
    plt.bar(courses, values, color ='purple',
            width = 0.4)

    plt.xlabel("Types of Emotions")
    plt.ylabel("Emotions count")
    plt.title("Reviewer's emotions")
    plt.show()

def graph_for_total_words(count_of_words, UniqueNames):
    for i in range(len(count_of_words)):
        data = count_of_words[i]
        courses = (data.keys())
        values = (data.values())

        fig = plt.figure(figsize = (10, 5))
        plt.bar(courses, values, color ='purple',
                width = 0.4)

        plt.xlabel("Types of Emotions")
        plt.ylabel("Emotions count")
        plt.title(UniqueNames[i])
        plt.show()

#prints graph for overall hotel rating across all 3 websites
def graph_for_overall_rating(overall_df, UniqueNames):
    overall_ratings = overall_df.groupby('Hotel Name').mean()
    hotel_ratings = {}
    for i in range(len(overall_ratings)):
        hotel_ratings.update({UniqueNames[i]:overall_ratings['Rating'][i]})
    data = hotel_ratings
    values = list(data.keys())
    courses =  list(data.values())
    c = ['red', 'yellow', 'black', 'blue', 'orange','purple','pink','yellow','magenta', '#eeefff', '#FF5733', '#77D4FF', '#DBAFFF','#AFFBFF','#FFF4AF','#FFDDAF','#FFAFFB', '#9B5B98', '#539195','#775E6D',]
    fig = plt.figure(figsize = (90, 40))
    plt.barh(values, courses, color =c)

    plt.ylabel("Hotel Names")
    plt.xlabel("Rating Score")
    plt.title("Overall Ratings")
    plt.show()

#prints graph for overall hotel cleanliness rating across all 3 websites
def graph_for_cleanliness_rating(ratings_df):
    ratings_df.rename(columns = {'Hotel Name':'Hotel_Name'}, inplace = True)
    sub_factor_sum = ratings_df.groupby('Hotel_Name').sum()
    unique_hotels= ratings_df.Hotel_Name.unique()
    hotel_ratings={}
    for i in range(len(sub_factor_sum)):
            hotel_ratings.update({unique_hotels[i]:sub_factor_sum['Cleanliness'][i]})
            
    data = hotel_ratings
    values = list(data.keys())
    courses =  list(data.values())
    c = ['#77D4FF']
    fig = plt.figure(figsize = (90, 40))
    plt.barh(values, courses, color =c)

    plt.ylabel("Hotel Names")
    plt.xlabel("Rating Score")
    plt.title("Cleanliness Ratings")
    plt.show() 
#prints graph for overall hotel service rating across all 3 websites
def graph_for_service_rating(ratings_df):
    ratings_df.rename(columns = {'Hotel Name':'Hotel_Name'}, inplace = True)
    sub_factor_sum = ratings_df.groupby('Hotel_Name').sum()
    unique_hotels= ratings_df.Hotel_Name.unique()
    hotel_ratings={}
    for i in range(len(sub_factor_sum)):
            hotel_ratings.update({unique_hotels[i]:sub_factor_sum['Service'][i]})
            
    data = hotel_ratings
    values = list(data.keys())
    courses =  list(data.values())
    c = ['#DBAFFF']
    fig = plt.figure(figsize = (90, 40))
    plt.barh(values, courses, color =c)

    plt.ylabel("Hotel Names")
    plt.xlabel("Rating Score")
    plt.title("Service Ratings")
    plt.show()

#function to plot frequency chart
def plot_frequency(freq):
    plt.figure(figsize=(10,5))
    freq.plot(50,cumulative=False)
    plt.show()

#function to plot word cloud
def plot_cloud(wordcloud):
    plt.figure(figsize=(40,30))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

#prints graph top 10 words for negative review
def top_nwords_graph(top10):
    data = dict(top10)
    courses = (data.keys())
    values =  (data.values())

    fig = plt.figure(figsize = (10, 5))

    # creating the bar plot
    plt.bar(courses, values, color ='blue',
            width = 0.4)

    plt.xlabel("Bad reviews")
    plt.ylabel("Number of times mentioned")
    plt.title("Total number of times mentioned")
    plt.show()
