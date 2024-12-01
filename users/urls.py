from django.contrib.auth.views import LogoutView
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import UserProfileView
from .views import CustomTokenObtainPairView
from .views import LoginView, RegisterView, UserViewSet, home

router = DefaultRouter()
router.register(r"users", UserViewSet)


urlpatterns = [
    path("", home, name="home"),  # 루트 페이지
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
]
