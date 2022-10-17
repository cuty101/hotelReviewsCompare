#imports
import multiprocessing

from flask import Flask, redirect, render_template

from functions import *

#app
app = Flask(__name__)



@app.route("/")
def hello():
    return render_template("menu.html")

@app.route("/top10words")
def top10words():
    job = multiprocessing.Process(target=top_words_graph, args=(p_top10_words,))
    job.start()
    return redirect("/")

@app.route("/top10wordswordcloud")
def toptenwordswordcloud():
    p_most_common = pd.Series(dict(p_top10_words))
    wordcloud = WordCloud(width=3000, height=2000, colormap="Set2", collocations=False, max_words=200)
    wordcloud.generate_from_frequencies(frequencies=p_most_common)
    job = multiprocessing.Process(target=plot_cloud, args=(wordcloud,))
    job.start()
    return redirect("/")

@app.route("/emotions")
def emotions():
    job = multiprocessing.Process(target=graph_for_reviewers_emotions, args=(p_list_of_unique_hotel_df,))
    job.start()
    return redirect("/")

@app.route("/overallrating")
def overallRating():
    job = multiprocessing.Process(target=graph_for_overall_rating, args=(df, p_UniqueNames,))
    job.start()
    return redirect("/")

@app.route("/cleanliness")
def cleanliness():
    job = multiprocessing.Process(target=graph_for_cleanliness_rating, args=(rating_df,))
    job.start()
    return redirect("/")

@app.route("/service")
def service():
    job = multiprocessing.Process(target=graph_for_service_rating, args=(rating_df,))
    job.start()
    graph_for_service_rating(rating_df)
    return redirect("/")

@app.route("/ntop10wordsgraph")
def ntop10wordsgraph():
    
    job = multiprocessing.Process(target=top_nwords_graph, args=(n_top10,))
    job.start()
    return redirect("/")

@app.route("/ntop10wordswordcloud")
def ntoptenwordswordcloud():
    n_most_common = pd.Series(dict(n_top10))
    wordcloud = WordCloud(width=3000, height=2000, colormap="Set2", collocations=False, max_words=200)
    wordcloud.generate_from_frequencies(frequencies=n_most_common)
    job = multiprocessing.Process(target=plot_cloud, args=(wordcloud,))
    job.start()
    return redirect("/")

    

@app.route("/nemotions")
def nemotions():
    job = multiprocessing.Process(target=graph_for_reviewers_emotions, args=(n_list_of_unique_hotel_df,))
    job.start()
    return redirect("/")

@app.route("/noverallrating")
def noverallrating():
    job = multiprocessing.Process(target=graph_for_overall_rating, args=(neg_df, n_UniqueNames))
    job.start()
    return redirect("/")
if __name__ == "__main__":
    nltk.download(["stopwords", "punkt", "wordnet"])
    df = pd.read_csv(r"all_reviews.csv")
    rating_df = pd.read_csv(r"all_subratings.csv") 
    
    #positive reviews analysis
    pos_df = pos_reviews(df)
    p_top10_words = clean_words(pos_df)
    p_filtered_reviews=filtered_reviews_based_on_top10(p_top10_words, pos_df)

    p_first_top_df=separate_reviews(p_filtered_reviews,p_top10_words)[0]
    p_second_top_df=separate_reviews(p_filtered_reviews,p_top10_words)[1]
    p_third_top_df=separate_reviews(p_filtered_reviews,p_top10_words)[2]
    p_fourth_top_df=separate_reviews(p_filtered_reviews,p_top10_words)[3]
    p_fifth_top_df=separate_reviews(p_filtered_reviews,p_top10_words)[4]
    p_sixth_top_df=separate_reviews(p_filtered_reviews,p_top10_words)[5]
    p_seventh_top_df=separate_reviews(p_filtered_reviews,p_top10_words)[6]
    p_eighth_top_df=separate_reviews(p_filtered_reviews,p_top10_words)[7]
    p_ninth_top_df=separate_reviews(p_filtered_reviews,p_top10_words)[8]
    p_tenth_top_df=separate_reviews(p_filtered_reviews,p_top10_words)[9]

    p_first_top_df=convert_to_dataframe(p_first_top_df, pos_df)
    p_first_top_df['Popular_Word']='room'
    print("5%")

    p_second_top_df=convert_to_dataframe(p_second_top_df, pos_df)
    p_second_top_df['Popular_Word']='staff'
    print("10%")

    p_third_top_df=convert_to_dataframe(p_third_top_df, pos_df)
    p_third_top_df['Popular_Word']='stay'
    print("15%")

    p_fourth_top_df=convert_to_dataframe(p_fourth_top_df, pos_df)
    p_fourth_top_df['Popular_Word']='service'
    print("20%")

    p_fifth_top_df=convert_to_dataframe(p_fifth_top_df, pos_df)
    p_fifth_top_df['Popular_Word']='location'
    print("25%")

    p_sixth_top_df=convert_to_dataframe(p_sixth_top_df, pos_df)
    p_sixth_top_df['Popular_Word']='friendly'
    print("30%")

    p_seventh_top_df=convert_to_dataframe(p_seventh_top_df, pos_df)
    p_seventh_top_df['Popular_Word']='clean'
    print("35%")

    p_eighth_top_df=convert_to_dataframe(p_eighth_top_df, pos_df)
    p_eighth_top_df['Popular_Word']='nice'
    print("40%")

    p_ninth_top_df=convert_to_dataframe(p_ninth_top_df, pos_df)
    p_ninth_top_df['Popular_Word']='breakfast'
    print("45%")

    p_tenth_top_df=convert_to_dataframe(p_tenth_top_df, pos_df)
    p_tenth_top_df['Popular_Word']='food'
    print("50%")

    p_unique_df = concat_dataframes_get_unique_hotels(p_first_top_df, p_second_top_df,p_third_top_df,p_fourth_top_df,p_fifth_top_df,p_sixth_top_df,p_seventh_top_df,p_eighth_top_df,p_ninth_top_df,p_tenth_top_df)

    #get unique hotel names
    p_UniqueNames = p_unique_df.Hotel_Name.unique()

    #create a data frame dictionary to store your data frames
    p_UniqueHotel = {elem : pd.DataFrame() for elem in p_UniqueNames}

    for key in p_UniqueHotel.keys():
       p_UniqueHotel[key] = p_unique_df[:][p_unique_df.Hotel_Name == key]

    p_list_of_unique_hotel_df=unique_hotels_df(p_UniqueNames, p_UniqueHotel)
    
    neg_df = neg_reviews(df)
    n_top10 = clean_words(neg_df)
    
    n_top10_words=[]
    for i in n_top10:
        n_top10_words.append(i[0])
    n_list=[]
    for review in neg_df['Content']:
        for i in n_top10:
            if i[0] in review:
                n_list.append(review)
                break
    n_filtered_review = pd.DataFrame(n_list)

    #['room', 'staff', 'check', 'service', 'stay', 'breakfast', 'time', 'nt', 'bed', 'even']
    n_room_reviews = []
    n_staff_reviews = []
    n_check_reviews = []
    n_service_reviews = []
    n_stay_reviews = []
    n_breakfast_reviews = []
    n_time_reviews = []
    n_nt_reviews = []
    n_bed_reviews = []
    n_even_reviews = []

    for review in n_filtered_review[0]:
        for j in range(len(n_top10_words)):
            if j == 0:
                if n_top10_words[j] in review:
                    n_room_reviews.append(review)
            elif j == 1:
                if n_top10_words[j] in review:
                    n_staff_reviews.append(review)
            elif j == 2:
                if n_top10_words[j] in review:
                    n_check_reviews.append(review)
            elif j == 3:
                if n_top10_words[j] in review:
                    n_service_reviews.append(review)
            elif j == 4:
                if n_top10_words[j] in review:
                    n_stay_reviews.append(review)
            elif j == 5:
                if n_top10_words[j] in review:
                    n_breakfast_reviews.append(review)
            elif j == 6:
                if n_top10_words[j]in review:
                    n_time_reviews.append(review)
            elif j == 7:
                if n_top10_words[j]in review:
                    n_nt_reviews.append(review)
            elif j == 8:
                if n_top10_words[j]in review:
                    n_bed_reviews.append(review)
            elif j == 9:
                if n_top10_words[j]in review:
                    n_even_reviews.append(review)
    #['room', 'staff', 'check', 'service', 'stay', 'breakfast', 'time', 'nt', 'bed', 'even']
    
    n_room_review = pd.DataFrame(n_room_reviews)
    n_staff_review = pd.DataFrame(n_staff_reviews)
    n_check_review = pd.DataFrame(n_check_reviews)
    n_service_review = pd.DataFrame(n_service_reviews)
    n_stay_review = pd.DataFrame(n_stay_reviews)
    n_breakfast_review = pd.DataFrame(n_breakfast_reviews)
    n_time_review = pd.DataFrame(n_time_reviews)
    n_nt_review = pd.DataFrame(n_nt_reviews)
    n_bed_review = pd.DataFrame(n_bed_reviews)
    n_even_review = pd.DataFrame(n_even_reviews)
    
    n_unique_hotel_name=[]
    for hotel in neg_df['Hotel Name']:
            n_unique_hotel_name.append(hotel)
    n_unique_hotel_name=set(n_unique_hotel_name) 

    n_room_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    for i in n_room_review[0]:
        n_room_df= pd.concat([n_room_df,neg_df.loc[neg_df['Content']==i]])
    n_room_df['Popular_Word'] = 'room'
    n_room_df.sort_values(by=['Hotel Name'])
    print("55%")

    n_staff_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    for i in n_staff_review[0]:
        n_staff_df= pd.concat([n_staff_df,neg_df.loc[neg_df['Content']==i]])
    n_staff_df['Popular_Word'] = 'room'
    n_staff_df.sort_values(by=['Hotel Name'])
    print("60%")
    
    n_check_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    for i in n_check_review[0]:
        n_check_df= pd.concat([n_check_df,neg_df.loc[neg_df['Content']==i]])
    n_check_df['Popular_Word'] = 'nt'
    n_check_df.sort_values(by=['Hotel Name'])
    print("65%")
    
    n_service_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    for i in n_service_review[0]:
        n_service_df= pd.concat([n_service_df,neg_df.loc[neg_df['Content']==i]])
    n_service_df['Popular_Word'] = 'call'
    n_service_df.sort_values(by=['Hotel Name'])
    print('70%')

    n_stay_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    for i in n_stay_review[0]:
        n_stay_df= pd.concat([n_stay_df,neg_df.loc[neg_df['Content']==i]])
    n_stay_df['Popular_Word'] = 'breakfast'
    n_stay_df.sort_values(by=['Hotel Name'])
    print("75%")
    
    n_breakfast_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    for i in n_breakfast_review[0]:
        n_breakfast_df= pd.concat([n_breakfast_df,neg_df.loc[neg_df['Content']==i]])
    n_breakfast_df['Popular_Word'] = 'night'
    n_breakfast_df.sort_values(by=['Hotel Name'])
    print("80%")
    
    n_time_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    for i in n_time_review[0]:
        n_time_df= pd.concat([n_time_df,neg_df.loc[neg_df['Content']==i]])
    n_time_df['Popular_Word'] = 'staff'
    n_time_df.sort_values(by=['Hotel Name'])
    print("85%")
    
    n_nt_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    for i in n_nt_review[0]:
        n_nt_df= pd.concat([n_nt_df,neg_df.loc[neg_df['Content']==i]])
    n_nt_df['Popular_Word'] = 'taxi'
    n_nt_df.sort_values(by=['Hotel Name'])
    print("90%")
    
    n_bed_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    for i in n_bed_review[0]:
        n_bed_df= pd.concat([n_bed_df,neg_df.loc[neg_df['Content']==i]])
    n_bed_df['Popular_Word'] = 'even'
    n_bed_df.sort_values(by=['Hotel Name'])
    print("95%")
    
    n_even_df = pd.DataFrame(columns=['Hotel Name', 'Title', 'Content','Rating','Date of stay'])
    for i in n_even_review[0]:
        n_even_df= pd.concat([n_even_df,neg_df.loc[neg_df['Content']==i]])
    n_even_df['Popular_Word'] = 'stayed'
    n_even_df.sort_values(by=['Hotel Name'])
    print("100%!")
    
    #['room', 'staff', 'check', 'service', 'stay', 'breakfast', 'time', 'nt', 'bed', 'even']
    n_unique_df = concat_dataframes_get_unique_hotels(n_room_df, n_staff_df,n_check_df,n_service_df,n_stay_df,n_breakfast_df,n_time_df,n_nt_df,n_bed_df,n_even_df)

     #get unique hotel names
    n_UniqueNames = n_unique_df.Hotel_Name.unique()

    #create a data frame dictionary to store your data frames
    n_UniqueHotel = {elem : pd.DataFrame() for elem in n_UniqueNames}

    for key in n_UniqueHotel.keys():
        n_UniqueHotel[key] = n_unique_df[:][n_unique_df.Hotel_Name == key]
    n_list_of_unique_hotel_df=unique_hotels_df(n_UniqueNames, n_UniqueHotel)

    app.run()