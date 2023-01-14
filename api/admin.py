from django.contrib import admin
from .models import Book,BookComment,UserWishing

admin.site.register(Book)
admin.site.register(BookComment)
admin.site.register(UserWishing)

# Register your models here.
