from django.db import models
from django.contrib.auth.models import User

#Django provides a built in User model that provides basics user table proprety
#In this we eill not create another user table but we eill use the existing user model and 
#Instead of using state we will use groups models for best relationship model
#Django also provides a DRF django rest framework for building api's and this framework
#provides a session handling bay default, so we will use Token authentification instead of session authentification
# and JWT package will be used

# So we go ahead with Book table

class Book(models.Model):
	id = models.AutoField(primary_key=True) # primary_key parameter set to true mean taht this field is the key
	book_name = models.CharField(max_length=50)
	publish_date = models.DateTimeField()
	publisher = models.CharField(max_length=50)
	edition = models.CharField(max_length=20)
	language = models.CharField(max_length=20)
	author = models.CharField(max_length=50)
	ISBN = models.CharField(max_length=15)
	translator = models.CharField(max_length=50, null=True, blank=True) # to allow null we specify null params to true
	pages = models.IntegerField(default=0)
	price = models.IntegerField(default=0)
	book_state = models.BooleanField(default=False) #instead of using int, we use boolean which by convention 0 true 1 false
	intro = models.TextField() #text fiel do not have max_length as char_field
	intro_img = models.TextField()

class BookComment(models.Model):
	id = models.AutoField(primary_key=True)
	book_id = models.ForeignKey(Book, on_delete=models.CASCADE) # comment must be related to a book so we use foreign_key to express that relation 
	comments = models.TextField()
	levels = models.IntegerField(default=0)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	post_date = models.DateTimeField(auto_now=True) # we set auto_now parameter to true comment takes by efaut the current time it posted


class UserWishing(models.Model):
	id = models.AutoField(primary_key=True)
	book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
	type = models.IntegerField(default=0)
	add_date = models.DateTimeField(auto_now=True)





