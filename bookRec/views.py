from django.shortcuts import render, redirect
import pandas as pd 
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from torch import cosine_similarity
from .serializers import UserSerializer, BookSerializer, GenreSerializer
from .models import Book, Genre, UserBook, User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Avg
from surprise import Dataset
from surprise.model_selection import train_test_split
from surprise import SVD
from surprise import Reader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
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
from .recommendation_logic import recommend2, recommend
from sklearn.metrics import mean_squared_error



from django.conf import settings
import os


# load dataset
CSV_FILENAME = 'bookRec.csv'

def load_csv_data():
    # Get the path to the directory where 'bookRec.csv' is located
    csv_directory = os.path.join(settings.BASE_DIR, 'bookRec')
    
    # Construct the full path to the CSV file
    csv_path = os.path.join(csv_directory, CSV_FILENAME)
    
    # Load the CSV data into a DataFrame
    df = pd.read_csv(csv_path)
    
    return df

# Example usage
df = load_csv_data()
#print(books)

# filter columns
books = ['book', 'author', 'description', 'genres','avg_rating','num_ratings']
df = df[books]

#df = pd.DataFrame(books)

# get first n genres from the list
n = 3
df[['genre1', 'genre2', 'genre3', 'genre4']] = df['genres'].str.split(',', n, expand=True)
#df = pd.DataFrame(books)

# drop unwanted columns
unwanted = ['genres', 'genre4']
df.drop(unwanted, axis=1, inplace=True)

# clean Genres
patt = r"[a-zA-Z]+"
gen_cols = ['genre1', 'genre2', 'genre3']
for g in gen_cols:
    df[g] = df[g].apply(lambda x: " ".join(re.findall("[a-zA-Z]+", str(x))))
    
    
# drop NULLs & reset index
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)



# Function to create the user-item matrix
def create_user_item_matrix():
    users = User.objects.all()
    books = Book.objects.all()
    
    user_item_matrix = np.full((len(users), len(books)), np.nan)
    user_index_map = {user.id: i for i, user in enumerate(users)}
    book_index_map = {book.id: i for i, book in enumerate(books)}
    
    user_book_ratings = UserBook.objects.all()
    
    for rating in user_book_ratings:
        user_index = user_index_map[rating.user__id]
        book_index = book_index_map[rating.book__id]
        user_item_matrix[user_index, book_index] = rating.rating
    
    return user_item_matrix

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # Convert _id to string and include it in the token payload
        user_id_str = str(request.user.id)
        response.data['user_id'] = user_id_str
        return response
    
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        # print("####################",serializer.data,"####################")
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({'access_token': access_token, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        login(request, user)
        serializer = UserSerializer(user) # Replace with your user retrieval logic

        refresh = RefreshToken.for_user(user)
        
        # token['user_id'] = str(user._id)
        access_token = str(refresh.access_token)
        refresh_token_str = str(refresh)
        return Response({'access_token': access_token, 'refresh': refresh_token_str, 'user_id': user.id,   'user': serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'success': 'Logged out successfully'})

     
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
@api_view(['GET'])
def get_books(req): 
    paginator = PageNumberPagination()
    paginator.page_size = 9  # Set the number of books per page
    
    books = Book.objects.all()
    result_page = paginator.paginate_queryset(books, req)
    
    serializer = BookSerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def get_books_by_keyword(request):
    
    try:
        keyword = request.GET.get('keyword')
        # Filter books based on the keyword
        books = Book.objects.filter(book__icontains=keyword)  # Adjust the field based on your model

        # Create a response with book details
        book_list = [{
            'id': book.id,
            'title': book.book,
            'author': book.author,
            'genres': book.genres
            # Add more details as needed
        } for book in books]

        return Response({'books': book_list})
    except Exception as e:
        return Response({'error': f'Error fetching books by keyword: {str(e)}'}, status=500)
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    
    

@require_POST
@csrf_exempt  # For demonstration purposes; use of CSRF protection in production
def save_book(request):
    # Assuming you have the authenticated user, retrieve the user and book information
    user_id = request.POST.get('userId')
    book_id = request.POST.get('bookId')  # Adjust this based on how you send the data from the front end
    rating = request.POST.get('rating')
    try:
        # Create a UserBook instance to associate the user with the book
        UserBook.objects.create(user_id=user_id, book_id=book_id, rating = rating)
        return JsonResponse({'message': 'Book saved successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def get_saved_books(request):
    user_id = request.GET.get('userId')  # Assuming you have a logged-in user
    saved_books = UserBook.objects.filter(user_id=user_id).values('book__id', 'book__book', 'book__author', 'book__description', 'book__genres', 'rating')  # Add other fields as needed
    return JsonResponse({'user_id': user_id, 'saved_books': list(saved_books)})


@api_view(['POST'])
def remove_saved_book(request):
    user_id = request.data.get('userId')
    book_id = request.data.get('bookId')
    print(user_id, type(user_id),'other',book_id, type(book_id))
    try:
        # Convert user_id and book_id to ObjectId
        
        
        print(f'user_id: {user_id, type(user_id)}, book_id: {book_id}')
        # Your logic to remove the book from the database
        saved_book = UserBook.objects.filter(user_id=user_id, book_id=book_id).first()

        if saved_book:
            saved_book.delete()
            return JsonResponse({'message': 'Book removed successfully'})
        else:
            return JsonResponse({'error': 'Saved book not found or not saved to the database'}, status=404)

    except Exception as e:
        return JsonResponse({'error': f'Error removing saved book: {str(e)}'}, status=500)



@api_view(['GET'])
def get_book_recommendations(request):
    try:
        # Fetch books with the highest average ratings (you can customize this logic)
        recommended_books = Book.objects.order_by('-avg_rating')[:15]

        # Create a response with recommended book details
        recommendations = [{
            'bookId': book.id,
            'bookTitle': book.book,
            'bookDescription': book.description,
            'rating': book.avg_rating
            # Add more details as needed
        } for book in recommended_books]

        return Response({'recommendations': recommendations})
    except Exception as e:
        return Response({'error': f'Error fetching book recommendations: {str(e)}'}, status=500)


@require_GET
@csrf_exempt
def get_recommendations(request):
    try:
        author = request.GET.get('author')
        title = request.GET.get('title')
        recommendations = recommend2(author, title, df)

        formatted_recommendations = [{'bookTitle': recommendation} for recommendation in recommendations]
        return JsonResponse({'recommendations': formatted_recommendations})
    except Exception as e:
        return JsonResponse({'error': f'Error fetching recommendations: {str(e)}'}, status=500)
    
@require_GET
@csrf_exempt
def get_recommendations_genre(request):
    try:
        genre = request.GET.get('genre')
        title = request.GET.get('title')
        recommendations = recommend( title,genre, df)

        formatted_recommendations = [{'bookTitle': recommendation} for recommendation in recommendations]
        return JsonResponse({'recommendations': formatted_recommendations})
    except Exception as e:
        return JsonResponse({'error': f'Error fetching recommendations: {str(e)}'}, status=500)
    


# Collaborative filtering function
def collaborative_filtering_predict(user_item_matrix, user_index):
    # Calculate cosine similarity between users
    user_similarity_matrix = cosine_similarity(user_item_matrix)

    # Predict ratings for the target user
    weighted_sum = np.dot(user_similarity_matrix[user_index], user_item_matrix)
    sum_of_similarities = np.sum(user_similarity_matrix[user_index])
    predicted_ratings = weighted_sum / (sum_of_similarities + 1e-8)
    predicted_ratings[user_item_matrix[user_index].nonzero()] = 0
    
    return predicted_ratings

def collaborative_filtering_recommendations(request):
    # Split data into training and testing sets
    user_item_matrix = create_user_item_matrix()
    train_matrix, test_matrix = train_test_split(user_item_matrix, test_size=0.2, random_state=42)

    # Example: Predict ratings for User with index 0 on the test set
    user_index = 0
    predicted_ratings = collaborative_filtering_predict(train_matrix, user_index)

    # Evaluate the model on the test set
    true_ratings = test_matrix.flatten()
    predicted_ratings = collaborative_filtering_predict(train_matrix, user_index).flatten()

    # Calculate mean squared error as a simple evaluation metric
    mse = mean_squared_error(true_ratings[~np.isnan(true_ratings)], predicted_ratings[~np.isnan(true_ratings)])
    
    # Display predicted ratings
    predictions = []
    for i, rating in enumerate(predicted_ratings):
        book_name = Book.objects.all()[i].book
        predictions.append({'book': book_name, 'rating': round(rating, 2)})

    return JsonResponse({'predictions': predictions, 'mse': round(mse, 2)})