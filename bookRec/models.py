from djongo import models
from bson import ObjectId
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, username,  password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,username,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email,username, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    id = models.CharField(max_length=24, unique=True, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=500, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Establishing a relationship many-to-many btwn user and book
    books = models.ManyToManyField('Book', related_name='users', blank=True, through='UserBook')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
    def save(self, *args, **kwargs):
        # Set the 'id' field to the string representation of '_id'
        self.id = str(self._id)
        super().save(*args, **kwargs)

 
class Book(models.Model):
    id =  models.BigAutoField(auto_created=True, primary_key=True, null=True, serialize=False, verbose_name='ID'),
    book = models.CharField(max_length=250)
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    genres = models.CharField(max_length=250)
    avg_rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    num_ratings = models.CharField(max_length=25)
    url = models.CharField(max_length=500)
    
    def __str__(self) : 
       return self.book
   
class UserBook(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    id = models.CharField(max_length=24, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0) 

    def __str__(self):
        return f'{self.user.username} - {self.book.title} - {self.rating}'
   
    class Meta:
        unique_together = ('user', 'book', 'rating')
    def save(self, *args, **kwargs):
        # Set the 'id' field to the string representation of '_id'
        self.id = str(self._id)
        super().save(*args, **kwargs)
        
        
class Genre(models.Model):
    id =  models.BigAutoField(auto_created=True, primary_key=True, null=True, serialize=False, verbose_name='ID'),
    genre = models.CharField(max_length=100)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# class user_profile(models.Model): 
#     uusername = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=500, blank=False)
    
#     USERNAME_FIELD = 'email'
    
#     def __str__(self) : 
#        return self.book
    # Create your models here.
# class Feature(models.Model):
#     name = models.CharField(max_length=100) 
#     details =  models.TextField(default='',max_length=500)
    
# class AppUserManager(BaseUserManager): 
#     def create_user(self, email, password=None):
#         if not email: 
#             raise ValueError('An email is required.')
#         if not password: 
#             raise ValueError(' A password is required. ')
#         email = self.normalize_email(email)
#         user = self.model(email = email)
#         user.set_password(password)
#         user.save()
#         return user  
#     def create_super_user(self, email, password=None): 
#         if not email: 
#             raise ValueError('An email is required.')
#         if not password: 
#             raise ValueError(' A password is required. ')
#         user = self.create_user(email, password)
#         user.is_superuser = True
#         user.save()
#         return user
    
# class AppUser(AbstractBaseUser,PermissionsMixin):
#     # user_id = models.BigAutoField(primary_key=True)
#     email = models.EmailField(max_length=50, unique=True) 
#     username = models.CharField(max_length=50 )
#     USERNAME_FIELD= 'email'
#     REQUIRED_FIELDS = ['username']
#     objects = AppUserManager()
#     #returns a username when a user obj is created
#     def __str__(self): 
#         return self.username
        
    
# class User(models.Model): 
#     username = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=500, blank=False)
    
#     USERNAME_FIELD = 'email '
#     def __str__(self) : 
#        return self.email


