from django.urls import path, include
from . import views


# list that gonna take all the urls of our project
urlpatterns = [
    path('api/', include('bookRec.api.urls')),
    path('home/', views.HomeView.as_view(), name ='home'), 
    path('logout/', views.LogoutView.as_view(), name ='logout')
    
]