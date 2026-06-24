from django.urls import path
from .views import (
    QuestionListAPIView, AnswerSubmitAPIView, MatchListAPIView,
    SendFriendRequestAPIView, RespondFriendRequestAPIView, ReceivedRequestsAPIView,
    MyMatchListAPIView, ChatMessageAPIView, PaymentVerifyAPIView
)

urlpatterns = [
    # 질문/답변/추천
    path('questions/', QuestionListAPIView.as_view()),
    path('answers/', AnswerSubmitAPIView.as_view()),
    path('matches/recommend/', MatchListAPIView.as_view()),   # 추천 이성 목록 (이름 변경)

    # 친구요청
    path('friend-request/send/', SendFriendRequestAPIView.as_view()),
    path('friend-request/respond/', RespondFriendRequestAPIView.as_view()),
    path('friend-request/received/', ReceivedRequestsAPIView.as_view()),

    # 채팅
    path('my-matches/', MyMatchListAPIView.as_view()),                       # 내 채팅방 목록
    path('matches/<int:match_id>/messages/', ChatMessageAPIView.as_view()),  # 채팅

    # 결제
    path('payment/verify/', PaymentVerifyAPIView.as_view()),
]