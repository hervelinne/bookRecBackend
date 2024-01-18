from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book, Genre, UserBook
# AppUser
# Register your models here.
# admin.site.register(Feature)
admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(UserBook)