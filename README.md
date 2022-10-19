# hotelReviewsCompare
A python project to retrieve english reviews, ratings of top hotels from online booking sites and present them
First, you need to install the required dependencies with
```
pip install -r requirements.txt  
```
Just clone this repo and run
```
python coolflaskapp.py  
```
wait for the program to run, then head over to 127.0.0.1:5000 and click the buttons and enjoy.

To use multiple data files:
```
pd.read_csv(r'C:\Users\chery\Desktop\python_proj\reviews.csv')
```
```
pd.concat([codex_df_ratings, verno_df_ratings, xinying_df_ratings])
```
```
concat_df.to_csv(r'C:\Users\chery\Desktop\python_proj\all_subratings.csv',index=False)
```
