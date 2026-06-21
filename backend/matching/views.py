from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer

from django.contrib.auth import get_user_model
from .similarity import calculate_similarity
from .models import Question

class QuestionListAPIView(generics.ListAPIView):
    """전체 질문 목록 (꼬리질문 포함) 반환"""
    queryset = Question.objects.all().prefetch_related('choices')
    serializer_class = QuestionSerializer


class AnswerSubmitAPIView(APIView):
    """
    유저가 답변을 한꺼번에 제출
    요청 예시:
    {
        "user_id": 1,
        "answers": [
            {"question": 1, "choice": 3},
            {"question": 2, "choice": 5},
            {"question": 5, "choice": 12},
            {"question": 5, "choice": 14}   # 복수선택
        ]
    }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user   # JWT로 인증된 유저
        answers = request.data.get('answers', [])

        # 재설문 대비: 기존 답변 삭제 후 재등록
        Answer.objects.filter(user=user).delete()

        created = []
        for item in answers:
            ans = Answer.objects.create(
                user=user,
                question_id=item['question'],
                choice_id=item['choice'],
            )
            created.append(ans.id)

        user.is_survey_done = True
        user.save()

        return Response(
            {'message': '답변 저장 완료', 'saved_count': len(created)},
            status=status.HTTP_201_CREATED
        )
    

User = get_user_model()

class MatchListAPIView(APIView):
    """
    나와 잘 맞는 이성 목록을 유사도 높은 순으로 반환.
    블라인드라 닉네임 정도만 노출.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        me = request.user

        if not me.is_survey_done:
            return Response({'error': '먼저 설문을 완료해주세요.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # 이성 + 설문 완료한 유저만 후보
        opposite = 'F' if me.gender == 'M' else 'M'
        candidates = User.objects.filter(
            gender=opposite, is_survey_done=True
        ).exclude(id=me.id)

        # 질문 캐싱 (반복 조회 방지)
        question_cache = {q.id: q for q in Question.objects.all()}

        results = []
        for other in candidates:
            score = calculate_similarity(me, other, question_cache)
            results.append({
                'user_id': other.id,
                'nickname': other.nickname,
                'birth_year': other.birth_year,
                'similarity': score,
            })

        # 유사도 높은 순 정렬
        results.sort(key=lambda x: x['similarity'], reverse=True)

        return Response({'matches': results[:20]})   # 상위 20명