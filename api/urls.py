from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()

router.register("users", UserViewSet)
router.register("book", BookViewSet)
router.register("book-comments", BookCommentViewSet)
router.register("wish-list", UserWishingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view())
]
