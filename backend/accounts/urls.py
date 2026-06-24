from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CompleteUploadJobAPIView, SignupAPIView, MyProfileAPIView,
    AIJobCreateAPIView, AIJobStatusAPIView,
    NextJobAPIView, CompleteJobAPIView,
)
urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),       # JWT 발급
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh'),# 토큰 갱신
    path('me/', MyProfileAPIView.as_view(), name='my-profile'),
        # 유저용
    path('ai/create/', AIJobCreateAPIView.as_view()),
    path('ai/status/<int:job_id>/', AIJobStatusAPIView.as_view()),
    # 워커용
    path('ai/next-job/', NextJobAPIView.as_view()),
    path('ai/complete/', CompleteJobAPIView.as_view()),
    path('ai/complete-upload/', CompleteUploadJobAPIView.as_view()),
]