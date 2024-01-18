from .models import Book, Genre
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

User = get_user_model()
        
class UserSerializer(serializers.ModelSerializer):
    # Marked as write_only, so when you serialize a User object using this serializer, 
    # the hashed password won't be included in the output. It's only used when creating or updating a user through the API.
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
  
    
    def create(self, validated_data) : 
        password = validated_data.pop('password', None)
        user = User.objects.create_user(password=password, **validated_data)
        return user
    

class BookSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Book 
        fields =  '__all__'
     
class GenreSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Genre 
        fields =  '__all__'   

       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       


















# from django.contrib.auth import get_user_model, authenticate
# from django.core.exceptions import ValidationError     
# class UserRegisterSerializer(serializers.ModelSerializer): 
#     class Meta: 
#         model= UserModel
#         fields = '__all__'
#     def create(self, clean_data) : 
#         user_obj = UserModel.objects.create_user(email=clean_data['email'], 
#                                                  password=clean_data['password'])
#         user_obj.username = clean_data['username']
#         user_obj.save()
#         return user_obj
    
# class UserLoginSerializer(serializers.Serializer): 
#     email = serializers.EmailField()
#     password = serializers.CharField()
#     ##
#     def checkUser(self, clean_data):  
#         user = authenticate(username = clean_data['email'], password = clean_data['password'])
#         if not user : 
#             raise ValidationError('user not found')
#         return user 
# class CustomTokenSerializer(serializers.Serializer):
#     refresh = serializers.CharField()
#     access = serializers.CharField()

  # def validate_password(self, value):
    #     # Use Django's built-in password validation
    #     validate_password(value)
    #     return value