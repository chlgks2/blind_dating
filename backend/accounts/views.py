from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .serializers import SignupSerializer, UserProfileSerializer

User = get_user_model()


class SignupAPIView(generics.CreateAPIView):
    """회원가입 - 누구나 접근 가능"""
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


class MyProfileAPIView(APIView):
    """내 정보 조회 - 로그인 필요 (request.user 사용)"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
