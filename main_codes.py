#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from gensim.parsing.porter import PorterStemmer
porter_stemmer = PorterStemmer()
from nltk.probability import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from nrclex import NRCLex
import collections, functools, operator
get_ipython().run_line_magic('run', 'functions.ipynb')


# In[2]:


df = pd.read_csv(r'C:\Users\chery\Desktop\python_proj\all_reviews.csv')

df


# In[3]:


neg_reviews(df)


# In[4]:


pos_df=pos_reviews(df)
pos_df


# In[5]:


rating_df=pd.read_csv(r'C:\Users\chery\Desktop\python_proj\all_subratings.csv')


# In[6]:


top10_words=clean_words(pos_df)


# In[7]:


top_words_graph(top10_words)


# In[8]:


filtered_reviews=filtered_reviews_based_on_top10(top10_words, pos_df)


# In[9]:


first_top_df=separate_reviews(filtered_reviews,top10_words)[0]


# In[10]:


second_top_df=separate_reviews(filtered_reviews,top10_words)[1]


# In[11]:


third_top_df=separate_reviews(filtered_reviews,top10_words)[2]


# In[12]:


fourth_top_df=separate_reviews(filtered_reviews,top10_words)[3]


# In[13]:


fifth_top_df=separate_reviews(filtered_reviews,top10_words)[4]


# In[14]:


sixth_top_df=separate_reviews(filtered_reviews,top10_words)[5]


# In[15]:


seventh_top_df=separate_reviews(filtered_reviews,top10_words)[6]


# In[16]:


eighth_top_df=separate_reviews(filtered_reviews,top10_words)[7]


# In[17]:


ninth_top_df=separate_reviews(filtered_reviews,top10_words)[8]


# In[18]:


tenth_top_df=separate_reviews(filtered_reviews,top10_words)[9]


# In[19]:


first_top_df=convert_to_dataframe(first_top_df, pos_df)
first_top_df['Popular_Word']='room'


# In[20]:


second_top_df=convert_to_dataframe(second_top_df, pos_df)
second_top_df['Popular_Word']='staff'


# In[21]:


third_top_df=convert_to_dataframe(third_top_df, pos_df)
third_top_df['Popular_Word']='stay'


# In[22]:


fourth_top_df=convert_to_dataframe(fourth_top_df, pos_df)
fourth_top_df['Popular_Word']='service'


# In[23]:


fifth_top_df=convert_to_dataframe(fifth_top_df, pos_df)
fifth_top_df['Popular_Word']='location'


# In[24]:


sixth_top_df=convert_to_dataframe(sixth_top_df, pos_df)
sixth_top_df['Popular_Word']='friendly'


# In[25]:


seventh_top_df=convert_to_dataframe(seventh_top_df, pos_df)
seventh_top_df['Popular_Word']='clean'


# In[26]:


eighth_top_df=convert_to_dataframe(eighth_top_df, pos_df)
eighth_top_df['Popular_Word']='nice'


# In[27]:


ninth_top_df=convert_to_dataframe(ninth_top_df, pos_df)
ninth_top_df['Popular_Word']='breakfast'


# In[28]:


tenth_top_df=convert_to_dataframe(tenth_top_df, pos_df)
tenth_top_df['Popular_Word']='food'


# In[29]:


unique_df=concat_dataframes_get_unique_hotels(first_top_df, second_top_df,third_top_df,fourth_top_df,fifth_top_df,sixth_top_df,seventh_top_df,eighth_top_df,ninth_top_df,tenth_top_df)


# In[30]:


#get unique hotel names
UniqueNames = unique_df.Hotel_Name.unique()

#create a data frame dictionary to store your data frames
UniqueHotel = {elem : pd.DataFrame() for elem in UniqueNames}

for key in UniqueHotel.keys():
   UniqueHotel[key] = unique_df[:][unique_df.Hotel_Name == key]


# In[31]:


list_of_unique_hotel_df=unique_hotels_df(UniqueNames)


# In[32]:


graph_for_reviewers_emotions(list_of_unique_hotel_df)


# In[34]:


graph_for_overall_rating(df, UniqueNames)


# In[36]:


graph_for_cleanliness_rating(rating_df)


# In[38]:


graph_for_service_rating(rating_df)


# In[ ]:




