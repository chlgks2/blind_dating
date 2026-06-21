from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupAPIView, MyProfileAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),       # JWT 발급
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh'),# 토큰 갱신
    path('me/', MyProfileAPIView.as_view(), name='my-profile'),
]