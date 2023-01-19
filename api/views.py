from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from django.db import transaction
from .serializers import *
from .models import *
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

class TokenPairView(TokenObtainPairView):
	serializer_class = TokenPairSerializer

class UserViewSet(mixins.ListModelMixin,
				mixins.RetrieveModelMixin,
				mixins.UpdateModelMixin,
				viewsets.GenericViewSet):
	authentication_classes = SessionAuthentication, JWTAuthentication
	permission_classes = IsAuthenticated,
	queryset = User.objects.all()
	serializer_class = UserSerializer

	@action(methods=["POST"], detail=False, url_name=r"register",url_path=r"register",permission_classes=[AllowAny], serializer_class=RegisterSerializer)
	def register(self, request):
		telephone = request.data.get('username')
		password=request.data.get('password')
		user = User(username=telephone)
		user.set_password(password)
		try:
			user.save()
			group=Group.objects.get(name="user")
			user.groups.add(group)
		except Exception as e:
			return Response({"details":"Username already taken"},500)
		return Response(201)

class GroupViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = IsAuthenticated,
	queryset = Group.objects.all().order_by('-id')
	serializer_class = GroupSerializer