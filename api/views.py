from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
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
from rest_framework import filters
from rest_framework.filters import SearchFilter
from django.db.models import Sum

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


class BookViewSet(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = IsAuthenticated,
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['book_state',]

	@action(methods=["GET"], detail=True, url_name=r"validate",url_path=r"validate",permission_classes=[IsAdminUser])
	def register(self, request,pk):
		book = self.get_object()
		book.book_state=True
		book.save()
		return Response(200)

	@action(methods=["GET"], detail=True, url_name=r"stats",url_path=r"stats",permission_classes=[IsAdminUser])
	def getBookStats(self, request,pk):
		book = self.get_object()
		q_comment = BookComment.objects.filter(book_id=book.id)
		book_comments = q_comment.count()
		book_score = q_comment.aggregate(Sum('levels')).get("levels__sum")
		book_read = UserWishing.objects.filter(book_id=book.id,type_wishing="R").count()
		book_wish_read = UserWishing.objects.filter(book_id=book.id,type_wishing="WR").count()

		return Response({
			"book":BookSerializer(book, many=False).data,
			"book_comments":book_comments,
			"book_score":book_score,
			"book_read":book_read,
			"book_wish_read":book_wish_read,
			},200)

	@action(methods=["GET"], detail=True, url_name=r"mark-read",url_path=r"mark-read",permission_classes=[IsAuthenticated])
	def markRead(self, request,pk):
		book = self.get_object()
		user_wishing = UserWishing(
			user_id = request.user,
			book_id = book,
			type_wishing = 'R'
			)
		user_wishing.save()
		return Response(200)

	@action(methods=["GET"], detail=True, url_name=r"mark-wish-read",url_path=r"mark-wish-read",permission_classes=[IsAuthenticated])
	def markWishRead(self, request,pk):
		book = self.get_object()
		user_wishing = UserWishing(
			user_id = request.user,
			book_id = book,
			type_wishing = 'WR'
			)
		user_wishing.save()
		return Response(200)

class BookCommentViewSet(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = IsAuthenticated,
	queryset = BookComment.objects.all()
	serializer_class = BookCommentSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ["book_id","levels","user_id",]

	def list(self, request, *args, **kwargs):
		#q = EmployeeSalary.objects.all().order_by('-salary')[1:1]
		queryset = BookComment.objects.all().reverse()[:5]
		serializer = BookCommentSerializer(queryset, many=True)
		return Response(serializer.data)

	@action(methods=["POST"], detail=False, url_name=r"fetch-more",url_path=r"fetch-more",permission_classes=[IsAuthenticated])
	def fetchMore(self, request):
		data = request.data
		book_id=Book.objects.get(id=data['book_id'])
		start=int(data['start'])
		queryset=BookComment.objects.all().reverse()[start:start+5]
		serializer = BookCommentSerializer(queryset, many=True)
		return Response(serializer.data)

class UserWishingViewSet(viewsets.ModelViewSet):
	authentication_classes = [JWTAuthentication, SessionAuthentication]
	permission_classes = IsAuthenticated,
	queryset = UserWishing.objects.all()
	serializer_class = UserWishingSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ["book_id","type_wishing","user_id",]

	@action(methods=["GET"], detail=False, url_name=r"fetch-wish",url_path=r"fetch-wish",permission_classes=[IsAuthenticated])
	def fetchWishList(self, request):
		read = list(UserWishing.objects.filter(type_wishing="R").values_list('book_id', flat=True))
		wish_read = list(UserWishing.objects.filter(type_wishing="WR").values_list('book_id', flat=True))
		
		book_read = BookSerializer(Book.objects.filter(id__in=read),many=True).data
		book_wish_read = BookSerializer(Book.objects.filter(id__in=wish_read), many=True).data


		return Response({
			"book_read":book_read,
			"book_wish_read":book_wish_read
			},200)
