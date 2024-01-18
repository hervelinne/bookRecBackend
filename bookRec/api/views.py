from ..models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.http import HttpResponse





    
# def post(request, mr):
#     return render(request, 'post.html', {'mr': mr})
    