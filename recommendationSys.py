import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import pickle




# READ THE DATABASE FILE 

movies = pd.read_csv("D:\satyam\minorProject\movieRecommendor\movies.csv")
credit = pd.read_csv("D:\satyam\minorProject\movieRecommendor\credits.csv")

#print(movies.head(1))
#print(credit.head(1))

# MERGING BOTH THE DATABASE FILE IN ONE FILE "MOVIE"

movie = movies.merge(credit, on="title")

# print(movie.shape)
# print(movie.head())

# print(movie.info())

# genres
# id
# keywords
# title
# overview
# cast
# crew

movies = movie[['movie_id','title','overview','genres','keywords','cast','crew']]


# print(movies.dropna(inplace=True))
# print(movies.isnull().sum())

def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name']) 
    return L 
    
movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)

def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
        counter+=1
    return L

movies['cast']=movies['cast'].apply(convert)

movies['cast'] = movies['cast'].apply(lambda x:x[0:3])

def fetch_director(text):
    L=[]
    for i in ast.literal_eval(text):
        if i['job']=='Director':
            L.append(i['name'])
            break
        return L

movies.sample(5)    

def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1

movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)
movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)


movies['overview']=movies['overview'].astype(str).apply(lambda x:x.split())

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new = movies.drop(columns=['overview','genres','keywords','cast','crew'])


new['tags'] = new['tags'].apply(lambda x: " ".join(x))




# movies['genres']=movie['genres'].apply(lambda x:[i.replace(" ","")for i in x])
# movies['keywords']=movie['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
# movies['cast']=movie['cast'].apply(lambda x:[i.replace(" ","")for i in x])
# movies['crew']=movie['crew'].apply(lambda x:[i.replace(" ","")for i in x])
# movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']

# new_df=movies[['movie_id','title','tags']]
# new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x).lower())
# print(new_df.head())

# movies['tags']=movies['tags'].apply(lambda x:x.lower())

# ps = PorterStemmer()
# def stem(text):
#     y=[]
#     for i in text.split():
#         y.append(ps.stem(i))

#     return " ".join(y)

# new_df['tags']= new_df['tags'].apply(stem)

cv=CountVectorizer(max_features=5000,stop_words='english')
vectors=cv.fit_transform(new['tags']).toarray()


similarity=cosine_similarity(vectors)


new['tags'] = new['tags'].apply(lambda x: " ".join(x))

def recommend(movie):
    index = new[new['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(new.iloc[i[0]].title)

# def recommend(movie):
#     movie_index=new_df[new_df['title']==movie].index[0]
#     distances = similarity[movie_index]
#     movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
#     for i in movies_list:
#         print(new_df.iloc[i[0]].title)
        

pickle.dump(new,open('movies.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))




