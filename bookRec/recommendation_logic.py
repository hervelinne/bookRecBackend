# standard libraries
import json # will be needed for saving preprocessing details
import numpy as np # for data manipulation & linear algebra
import pandas as pd # for data manipulation, data processing, CSV file I/O (e.g. pd.read_csv)
import re
import string
import random
import warnings
warnings.simplefilter('ignore')
import joblib # for saving algorithm and preprocessing objects
import seaborn as sns

# nltk 
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# sklearn 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split # will be used for data split
from sklearn.preprocessing import LabelEncoder # for preprocessing
from sklearn.ensemble import RandomForestClassifier # for training the algorithm
from sklearn.ensemble import ExtraTreesClassifier # for training the algorithm
from sklearn.feature_extraction.text import TfidfVectorizer  # For TF-IDF vectorization
from sklearn.metrics.pairwise import linear_kernel  # For computing cosine similarity



# logic for recommending books based on Book title. It takes book title and genre as an input.

def recommend(title, genre, df):
    # Matching the genre with the dataset and reset the index
    temp = df[(df['genre1'] == genre) | (df['genre2'] == genre) | (df['genre3'] == genre)]  
    temp.reset_index(level = 0, inplace = True) 
  
    # Convert the index into series
    indices = pd.Series(temp.index, index = temp['book'])
    
    #Converting the book title into vectors and used bigram
    tf = TfidfVectorizer(analyzer='word', ngram_range=(2, 2), min_df = 1, stop_words='english')
    tfidf_matrix = tf.fit_transform(temp['book'])
    
    # Calculating the similarity measures based on Cosine Similarity
    sg = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # Get the index corresponding to original_title
    idx = indices[title]
    
    # Get the pairwsie similarity scores 
    sig = list(enumerate(sg[idx]))
    
    # Sort the books
    sig = sorted(sig, key=lambda x: x[1], reverse=True)
    
    # Scores of the 5 most similar books 
    sig = sig[1:6]
    
    # Book indicies
    book_indices = [i[0] for i in sig]
   
    rec = temp[['book']].iloc[book_indices]
    recommendations = rec['book'].tolist()  # Return recommendations as a list
    return recommendations
# logic for recommending books based on Book Author & Title. It takes book title and genre as an input.


# Modify your recommend2 function to return the recommendations as a list
def recommend2(author, title, df):
    
    # get the unique genre list for the author
    temp_gen_lst = []
    gen_cols = ['genre1', 'genre2', 'genre3']
    for g in gen_cols:
        temp_gen_lst.append(df[df['author'] == author][g].unique().tolist())
        
    # flatten the list of list
    temp_gen_lst_flat = [item for sublist in temp_gen_lst for item in sublist]
        
    # de-duplicate the list
    temp_gen_lst_flat = list(set(temp_gen_lst_flat))
    
    # Matching the genre with the dataset and reset the index
    temp = df[(df['genre1'].isin(temp_gen_lst_flat)) | (df['genre2'].isin(temp_gen_lst_flat)) | (df['genre3'].isin(temp_gen_lst_flat))]  
    temp.reset_index(level = 0, inplace = True) 
  
    # Convert the index into series
    indices = pd.Series(temp.index, index = temp['book'])
    
    #Converting the book title into vectors and used bigram
    tf = TfidfVectorizer(analyzer='word', ngram_range=(2, 2), min_df = 1, stop_words='english')
    tfidf_matrix = tf.fit_transform(temp['book'])
    
    # Calculating the similarity measures based on Cosine Similarity
    sg = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # Get the index corresponding to original_title
    idx = indices[title]
    
    # Get the pairwsie similarity scores 
    sig = list(enumerate(sg[idx]))
    
    # Sort the books
    sig = sorted(sig, key=lambda x: x[1], reverse=True)
    
    # Scores of the 5 most similar books 
    sig = sig[1:6]
    
    # Book indicies
    book_indices = [i[0] for i in sig]

    rec = temp[['book']].iloc[book_indices]
    recommendations = rec['book'].tolist()  # Return recommendations as a list
    return recommendations
    
    
