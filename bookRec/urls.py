from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login_view, logout_view, signup_view, get_books, save_book, get_saved_books, remove_saved_book
from . import views

post_router = DefaultRouter()
#post_router.register(r'users', views.AppUser)
post_router.register(r'books', views.BookViewSet)
post_router.register(r'genres', views.GenreViewSet) 

# list that gonna take all the urls of our project
urlpatterns = [
   # path('', include('bookRec.urls')),
    path('api/', include(post_router.urls)),
    
    path('api/login/', login_view, name="login"),
    path('api/logout/', logout_view, name="logout"),
    path('api/signup/', signup_view, name="signup"),
    path('api/books_list/', get_books, name="book"),
    path('api/get_books_by_keyword/', views.get_books_by_keyword, name="get_books_by_keyword"),
    path('api/get_books_by_keyword_genre/', views.get_books_by_keyword_genre, name="get_books_by_keyword_genre"),
    path('api/save_book/', save_book, name='save_book'),
    path('api/get_saved_books/', get_saved_books, name='get_saved_books'),
    path('api/remove_saved_book/', remove_saved_book, name='remove_saved_book'),
    path('api/get_book_recommendations/', views.get_book_recommendations, name='get_book_recommendations'),
    path('api/get_recommendations/', views.get_recommendations, name='get_recommendations'),
    path('api/get_recommendations_genre/', views.get_recommendations_genre, name='get_recommendations_genre'),
    path('api/collaborative_filtering_recommendations/', views.collaborative_filtering_recommendations),
    
    
    
]