#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
        negative_reviews_df= pd.concat([negative_reviews_df,df.loc[df['Rating']==i]])
    negative_reviews_df.reset_index().drop(['index'], axis=1)
    
    return negative_reviews_df

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
        positive_reviews_df= pd.concat([positive_reviews_df,df.loc[df['Rating']==i]])
    positive_reviews_df
    
    return positive_reviews_df

def clean_words(pos_df):
    all_words = [word.lower() for sent in pos_df['Content'] for word in word_tokenize(sent)]
    #get top 10 words
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

def top_words_graph(top10):
    data = dict(top10)
    courses = (data.keys())
    values =  (data.values())

    fig = plt.figure(figsize = (10, 5))

    # creating the bar plot
    plt.bar(courses, values, color ='blue',
            width = 0.4)

    plt.xlabel("Good reviews")
    plt.ylabel("Number of times mentioned")
    plt.title("Top words for reviews")
    plt.show()
    
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

def convert_to_dataframe(review_list, pos_df):
    converted_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    for i in review_list[0]:
        converted_df= pd.concat([converted_df,pos_df.loc[pos_df['Content']==i]])
    converted_df.sort_values(by=['Hotel Name'])
    return converted_df

def concat_dataframes_get_unique_hotels(first_top_df, second_top_df,third_top_df,fourth_top_df,fifth_top_df,sixth_top_df,seventh_top_df,eighth_top_df,ninth_top_df,tenth_top_df):
    concatenated_dataframes = pd.concat([first_top_df, second_top_df,third_top_df,fourth_top_df,fifth_top_df,sixth_top_df,seventh_top_df,eighth_top_df,ninth_top_df,tenth_top_df])
    concatenated_dataframes=concatenated_dataframes.sort_values(by=['Hotel Name', 'Popular_Word'])
    concatenated_dataframes.rename(columns = {'Hotel Name':'Hotel_Name'}, inplace = True)
    
    return concatenated_dataframes


    
def unique_hotels_df(UniqueNames):
    list_of_df=[]
    for i in UniqueNames:
        df=UniqueHotel[i]
        df_unique= df[~df.index.duplicated(keep='first')]
        list_of_df.append(df_unique)
    return list_of_df

# def get_each_hotel_emotions(list_of_df):
#     emotion_for_each_hotel=[]
#     for k in range(len(list_of_df)):
#         happy_list=[]
#         angry_list=[]
#         surprised_list=[]
#         sad_list=[]
#         fear_list=[]
#         for i in list_of_df[k]['Content']:
#             emotion=get_emotion(i)
#             happy=[(k,v) for k,v in emotion.items()][0]
#             happy_list.append(happy)
#             angry=[(k,v) for k,v in emotion.items()][1]
#             angry_list.append(angry)
#             surprised=[(k,v) for k,v in emotion.items()][2]
#             surprised_list.append(surprised)
#             sad=[(k,v) for k,v in emotion.items()][3]
#             sad_list.append(sad)
#             fear=[(k,v) for k,v in emotion.items()][4]
#             fear_list.append(fear)

#             happyCount=0
#             for value in happy_list:
#                 happyCount=happyCount+value[1]
#             happyCount=happyCount*10

#             angryCount=0
#             for value in angry_list:
#                 angryCount=angryCount+value[1]
#             angryCount=angryCount*10

#             surprisedCount=0
#             for value in surprised_list:
#                 surprisedCount=angryCount+value[1]
#             surprisedCount=surprisedCount*10

#             sadCount=0
#             for value in sad_list:
#                 sadCount=sadCount+value[1]
#             sadCount=sadCount*10

#             fearCount=0
#             for value in fear_list:
#                 fearCount=fearCount+value[1]
#             fearCount=fearCount*10

#         emotions_count_dict={'Happy': round(happyCount,2), "Angry": round(angryCount,2), "Surprised": round(surprisedCount,2), "Sad": round(sadCount,2), "fear": round(fearCount,2)}
#         emotion_for_each_hotel.append(emotions_count_dict)
#     return emotion_for_each_hotel

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
    values =  (data.values())

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
        values =  (data.values())

        fig = plt.figure(figsize = (10, 5))
        plt.bar(courses, values, color ='purple',
                width = 0.4)

        plt.xlabel("Types of Emotions")
        plt.ylabel("Emotions count")
        plt.title(UniqueNames[i])
        plt.show()
        
def graph_for_overall_rating(overall_df, UniqueNames):
    overall_ratings = overall_df.groupby('Hotel Name').mean()
    hotel_ratings = {}
    for i in range(len(overall_ratings)):
        hotel_ratings.update({UniqueNames[i]:overall_ratings['Rating'][i]})
    data = hotel_ratings
    courses = (data.keys())
    values =  (data.values())
    c = ['red', 'yellow', 'black', 'blue', 'orange','purple','pink','yellow','magenta', '#eeefff', '#FF5733', '#77D4FF', '#DBAFFF','#AFFBFF','#FFF4AF','#FFDDAF','#FFAFFB', '#9B5B98', '#539195','#775E6D',]
    fig = plt.figure(figsize = (90, 40))
    plt.bar(courses, values, color =c,
            width = 0.4)

    plt.xlabel("Hotel Names")
    plt.ylabel("Rating Score")
    plt.title("Overall Ratings")
    plt.show()
    
def graph_for_cleanliness_rating(ratings_df):
    ratings_df.rename(columns = {'Hotel Name':'Hotel_Name'}, inplace = True)
    sub_factor_sum = ratings_df.groupby('Hotel_Name').sum()
    unique_hotels= ratings_df.Hotel_Name.unique()
    hotel_ratings={}
    for i in range(len(sub_factor_sum)):
            hotel_ratings.update({unique_hotels[i]:sub_factor_sum['Cleanliness'][i]})
            
    data = hotel_ratings
    courses = (data.keys())
    values =  (data.values())
    c = ['#77D4FF']
    fig = plt.figure(figsize = (90, 40))
    plt.bar(courses, values, color =c,
            width = 0.4)

    plt.xlabel("Hotel Names")
    plt.ylabel("Rating Score")
    plt.title("Cleanliness Ratings")
    plt.show() 
    

def graph_for_service_rating(ratings_df):
    ratings_df.rename(columns = {'Hotel Name':'Hotel_Name'}, inplace = True)
    sub_factor_sum = ratings_df.groupby('Hotel_Name').sum()
    unique_hotels= ratings_df.Hotel_Name.unique()
    hotel_ratings={}
    for i in range(len(sub_factor_sum)):
            hotel_ratings.update({unique_hotels[i]:sub_factor_sum['Service'][i]})
            
    data = hotel_ratings
    courses = (data.keys())
    values =  (data.values())
    c = ['#DBAFFF']
    fig = plt.figure(figsize = (90, 40))
    plt.bar(courses, values, color =c,
            width = 0.4)

    plt.xlabel("Hotel Names")
    plt.ylabel("Rating Score")
    plt.title("Service Ratings")
    plt.show()     
    
def top_nwords_graph(top10):
    data = dict(top10)
    courses = (data.keys())
    values =  (data.values())

    fig = plt.figure(figsize = (10, 5))

    # creating the bar plot
    plt.bar(courses, values, color ='blue',
            width = 0.4)

    plt.xlabel("Top 10 words")
    plt.ylabel("Number of times mentioned")
    plt.title("Bad reviews")
    plt.show()
    
def plot_frequency(freq):
    plt.figure(figsize=(10,5))
    freq.plot(50,cumulative=False)
    plt.show()

def plot_cloud(wordcloud):
    plt.figure(figsize=(40,30))
    plt.imshow(wordcloud)
    plt.axis("off")


# In[ ]:




