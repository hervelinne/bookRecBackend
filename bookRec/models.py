from django.db import models

# Create your models here.
# class Feature(models.Model):
#     name = models.CharField(max_length=100) 
#     details =  models.TextField(default='',max_length=500)
    
    
class User(models.Model): 
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50, blank=False)
    
    def __str__(self) : 
       return self.email