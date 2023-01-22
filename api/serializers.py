from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User,Group
from django.db import transaction
from .models import *

class TokenPairSerializer(TokenObtainPairSerializer):
	def validate(self, attrs):
		data = super(TokenPairSerializer, self).validate(attrs)
		data['groups'] = [group.name for group in self.user.groups.all()]
		data['username'] = self.user.username
		data['id'] = self.user.id
		data['is_admin'] = self.user.is_superuser
		data['first_name'] = self.user.first_name
		data['last_name'] = self.user.last_name
		return data

class GroupSerializer(serializers.ModelSerializer):

	class Meta:
		model = Group
		fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
	@transaction.atomic()
	def update(self,instance,validated_data):
		user = instance
		username = validated_data.get('username')
		nouv_password = validated_data.get('nouv_password')
		anc_password = validated_data.get('anc_password')
		if check_password(anc_password, self.context['request'].user.password):
			if username : user.username = username
			if first_name : user.first_name = first_name
			if last_name : user.last_name = last_name
			if password : user.set_password(password)
			user.save()
			return user
		return user
	class Meta:
		model = User
		read_only_fields = "is_active","is_staff"
		exclude = "last_login","is_staff","date_joined"

		extra_kwargs={
			'username':{
				'validators':[UnicodeUsernameValidator()]
			}
		}

class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)

    class Meta:
        fields = 'username', 'password'
        extra_kwargs={
            'username':{
                'validators':[UnicodeUsernameValidator()]
            },
            'password': {'write_only': True}
        }

class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = "__all__"
class BookCommentSerializer(serializers.ModelSerializer):

	def to_representation(self,instance):
		representation = super().to_representation(instance)
		representation['user_id'] = {
			'id':instance.user_id.id,
			'username':instance.user_id.username
		}
		return representation
	class Meta:
		model = BookComment
		fields = "__all__"
class UserWishingSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserWishing
		fields = "__all__"