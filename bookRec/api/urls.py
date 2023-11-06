from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import UserViewSet


# Create a router and register the UserViewSet
post_router = DefaultRouter()
post_router.register(r'users', UserViewSet)  # Use 'users' as the URL path

urlpatterns = [
    # ... other URL patterns ...
    path('api/', include(post_router.urls)),
]