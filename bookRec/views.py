from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class HomeView(APIView):
   permission_classes = (IsAuthenticated, )
   def get(self, request):
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)
    
class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)
           
           
           
           
           
           
           
           
           
           
# from .models import Feature

# Create your views here.
# def index(request): 
#     return HttpResponse('<h1>Hello world !</h1>')

# def index(request): 
#     features = Feature.objects.all()
#     return render(request, 'index.html', {'features' : features})

# def local(request): 
#     context ={
#         'name': "Mery", 'age':"23"}
#     return render(request, 'index.html', context)