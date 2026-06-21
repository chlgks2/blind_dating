from django.urls import path
from .views import QuestionListAPIView, AnswerSubmitAPIView, MatchListAPIView

urlpatterns = [
    path('questions/', QuestionListAPIView.as_view(), name='question-list'),
    path('answers/', AnswerSubmitAPIView.as_view(), name='answer-submit'),
    path('matches/', MatchListAPIView.as_view(), name='match-list'),
]