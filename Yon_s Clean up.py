#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import nltk
import matplotlib.pyplot as plt
import string
import numpy as np


from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from wordcloud import WordCloud
from gensim.parsing.porter import PorterStemmer
from nltk.probability import FreqDist
from nrclex import NRCLex
import collections, functools, operator
get_ipython().run_line_magic('run', 'functions.ipynb')
porter_stemmer = PorterStemmer()
filtered_sent=[]
stemmed_words=[]
all_words_clean = []

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


# In[2]:


df = pd.read_csv('all_reviews.csv')
df = neg_reviews(df)
df


# In[3]:


all_words = [word.lower() for sent in df['Content'] for word in word_tokenize(sent)]
print(all_words)


# In[4]:


#Specify stopword list
stopwords_english = set(stopwords.words('english'))
stopwords_english.update(['hotel', 'would', 'us','get','come','back','nt','could','good','great','one','rooms'])
#Create a new list of words by removing stopwords and punctuation from all_words

for word in all_words:
    if word not in stopwords_english and not word.isdigit():
        punc_free = ''.join([ch for ch in word if ch not in string.punctuation])
        if len(punc_free)>=2:
            # stem word to root word
            all_words_clean.append(punc_free)
print(all_words_clean)


# In[5]:



clean_words_frequency = FreqDist(all_words_clean)
top10 = clean_words_frequency.most_common(10)
most_common = clean_words_frequency.most_common(10)
most_common = pd.Series(dict(most_common))
most_common.plot()
wordcloud = WordCloud(width=3000, height=2000, colormap='Set2',collocations=False, max_words=200)
wordcloud.generate_from_frequencies(frequencies=most_common)

# Plot
plot_cloud(wordcloud)


# In[6]:


top10


# In[7]:


top_nwords_graph(top10)


# In[8]:


top10_words=[]
for i in top10:
    top10_words.append(i[0])
print(top10_words)
list=[]
for review in df['Content']:
    for i in top10:
        if i[0] in review:
            list.append(review)
            break
filtered_review = pd.DataFrame(list)
filtered_review


# In[9]:


#['room', 'staff', 'check', 'service', 'stay', 'breakfast', 'time', 'nt', 'bed', 'even']


room_reviews = []

staff_reviews = []

check_reviews = []

service_reviews = []

stay_reviews = []

breakfast_reviews = []

time_reviews = []

nt_reviews = []

bed_reviews = []

even_reviews = []

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
                check_reviews.append(review)
        elif j == 3:
            if top10_words[j] in review:
                service_reviews.append(review)
        elif j == 4:
            if top10_words[j] in review:
                stay_reviews.append(review)
        elif j == 5:
            if top10_words[j] in review:
                breakfast_reviews.append(review)
        elif j == 6:
            if top10_words[j]in review:
                time_reviews.append(review)
        elif j == 7:
            if top10_words[j]in review:
                nt_reviews.append(review)
        elif j == 8:
            if top10_words[j]in review:
                bed_reviews.append(review)
        elif j == 9:
            if top10_words[j]in review:
                even_reviews.append(review)
                


# In[10]:


#['room', 'staff', 'check', 'service', 'stay', 'breakfast', 'time', 'nt', 'bed', 'even']

room_review = pd.DataFrame(room_reviews)
staff_review = pd.DataFrame(staff_reviews)
check_review = pd.DataFrame(check_reviews)
service_review = pd.DataFrame(service_reviews)
stay_review = pd.DataFrame(stay_reviews)
breakfast_review = pd.DataFrame(breakfast_reviews)
time_review = pd.DataFrame(time_reviews)
nt_review = pd.DataFrame(nt_reviews)
bed_review = pd.DataFrame(bed_reviews)
even_review = pd.DataFrame(even_reviews)


# In[11]:


unique_hotel_name=[]
for hotel in df['Hotel Name']:
        unique_hotel_name.append(hotel)
unique_hotel_name=set(unique_hotel_name) 


# In[12]:


room_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
for i in room_review[0]:
    room_df= pd.concat([room_df,df.loc[df['Content']==i]])
room_df['Popular_Word'] = 'room'
room_df.sort_values(by=['Hotel Name'])


# In[13]:


staff_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
for i in staff_review[0]:
    staff_df= pd.concat([staff_df,df.loc[df['Content']==i]])
staff_df['Popular_Word'] = 'room'
staff_df.sort_values(by=['Hotel Name'])


# In[14]:


check_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
for i in check_review[0]:
    check_df= pd.concat([check_df,df.loc[df['Content']==i]])
check_df['Popular_Word'] = 'nt'
check_df.sort_values(by=['Hotel Name'])


# In[15]:


service_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
for i in service_review[0]:
    service_df= pd.concat([service_df,df.loc[df['Content']==i]])
service_df['Popular_Word'] = 'call'
service_df.sort_values(by=['Hotel Name'])


# In[16]:


stay_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
for i in stay_review[0]:
    stay_df= pd.concat([stay_df,df.loc[df['Content']==i]])
stay_df['Popular_Word'] = 'breakfast'
stay_df.sort_values(by=['Hotel Name'])


# In[17]:


breakfast_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
for i in breakfast_review[0]:
    breakfast_df= pd.concat([breakfast_df,df.loc[df['Content']==i]])
breakfast_df['Popular_Word'] = 'night'
breakfast_df.sort_values(by=['Hotel Name'])


# In[18]:


time_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
for i in time_review[0]:
    time_df= pd.concat([time_df,df.loc[df['Content']==i]])
time_df['Popular_Word'] = 'staff'
time_df.sort_values(by=['Hotel Name'])


# In[19]:


nt_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
for i in nt_review[0]:
    nt_df= pd.concat([nt_df,df.loc[df['Content']==i]])
nt_df['Popular_Word'] = 'taxi'
nt_df.sort_values(by=['Hotel Name'])


# In[20]:


bed_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
for i in bed_review[0]:
    bed_df= pd.concat([bed_df,df.loc[df['Content']==i]])
bed_df['Popular_Word'] = 'even'
bed_df.sort_values(by=['Hotel Name'])


# In[21]:


even_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
for i in even_review[0]:
    even_df= pd.concat([even_df,df.loc[df['Content']==i]])
even_df['Popular_Word'] = 'stayed'
even_df.sort_values(by=['Hotel Name'])


# In[22]:


print(even_df)


# In[23]:


#['room', 'staff', 'check', 'service', 'stay', 'breakfast', 'time', 'nt', 'bed', 'even']
unique_df = concat_dataframes_get_unique_hotels(room_df, staff_df,check_df,service_df,stay_df,breakfast_df,time_df,nt_df,bed_df,even_df)


# In[24]:


unique_df


# In[25]:


#get unique hotel names
UniqueNames = unique_df.Hotel_Name.unique()

#create a data frame dictionary to store your data frames
UniqueHotel = {elem : pd.DataFrame() for elem in UniqueNames}

for key in UniqueHotel.keys():
   UniqueHotel[key] = unique_df[:][unique_df.Hotel_Name == key]
list_of_unique_hotel_df=unique_hotels_df(UniqueNames)


# In[26]:


graph_for_reviewers_emotions(list_of_unique_hotel_df)


# In[27]:


graph_for_overall_rating(df, UniqueNames)


# In[ ]:




