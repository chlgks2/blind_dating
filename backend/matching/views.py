from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer

from django.contrib.auth import get_user_model
from .similarity import calculate_similarity
from .models import Question , FriendRequest, Match , Message
from .serializers import MessageSerializer
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
    
from .models import FriendRequest, Match


class SendFriendRequestAPIView(APIView):
    """친구요청 보내기. body: { "to_user": 5 }"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from_user = request.user
        to_user_id = request.data.get('to_user')

        if from_user.id == to_user_id:
            return Response({'error': '본인에게는 요청 불가'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({'error': '상대를 찾을 수 없음'}, status=404)

        # 이미 요청했는지 체크
        fr, created = FriendRequest.objects.get_or_create(
            from_user=from_user, to_user=to_user
        )
        if not created:
            return Response({'message': '이미 요청을 보냈습니다.'})

        return Response({'message': '친구요청 전송 완료'}, status=201)


class RespondFriendRequestAPIView(APIView):
    """받은 요청 수락/거절. body: { "request_id": 3, "action": "accept" }"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        req_id = request.data.get('request_id')
        action = request.data.get('action')   # 'accept' or 'reject'

        try:
            fr = FriendRequest.objects.get(id=req_id, to_user=user)
        except FriendRequest.DoesNotExist:
            return Response({'error': '요청을 찾을 수 없음'}, status=404)

        if action == 'accept':
            fr.status = FriendRequest.ACCEPTED
            fr.save()
            # 매칭 생성 (user_a는 id 작은 쪽으로 통일 → 중복방지)
            a, b = sorted([fr.from_user, fr.to_user], key=lambda u: u.id)
            match, _ = Match.objects.get_or_create(user_a=a, user_b=b)
            return Response({'message': '매칭 성립!', 'match_id': match.id})

        elif action == 'reject':
            fr.status = FriendRequest.REJECTED
            fr.save()
            return Response({'message': '거절했습니다.'})

        return Response({'error': 'action은 accept/reject'}, status=400)


class ReceivedRequestsAPIView(APIView):
    """내가 받은 대기중 요청 목록"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        reqs = FriendRequest.objects.filter(
            to_user=request.user, status=FriendRequest.PENDING
        )
        data = [{
            'request_id': r.id,
            'from_nickname': r.from_user.nickname,
            'from_user_id': r.from_user.id,
        } for r in reqs]
        return Response({'requests': data})

def get_user_matches_queryset(user):
    """내가 속한 매칭들"""
    from django.db.models import Q
    return Match.objects.filter(Q(user_a=user) | Q(user_b=user))


class MyMatchListAPIView(APIView):
    """내 매칭(채팅방) 목록"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        me = request.user
        matches = get_user_matches_queryset(me)
        data = []
        for m in matches:
            # 상대방 = 내가 아닌 쪽
            other = m.user_b if m.user_a == me else m.user_a
            last_msg = m.messages.last()
            data.append({
                'match_id': m.id,
                'other_nickname': other.nickname,
                'other_user_id': other.id,
                'last_message': last_msg.content if last_msg else None,
                'is_chat_open': m.is_chat_open,
            })
        return Response({'matches': data})


class ChatMessageAPIView(APIView):
    """
    GET  /matches/<match_id>/messages/  → 메시지 목록 조회 (폴링)
    POST /matches/<match_id>/messages/  → 메시지 전송  body: {"content": "안녕"}
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_match(self, user, match_id):
        """내가 참여한 매칭인지 검증"""
        try:
            match = Match.objects.get(id=match_id)
        except Match.DoesNotExist:
            return None
        if user != match.user_a and user != match.user_b:
            return None   # 내 채팅방이 아니면 접근 불가
        return match

    def get(self, request, match_id):
        match = self.get_match(request.user, match_id)
        if not match:
            return Response({'error': '접근 권한 없음'}, status=403)

        # ?after=<id> 로 특정 id 이후 메시지만 받기 (폴링 최적화)
        after_id = request.query_params.get('after')
        messages = match.messages.all()
        if after_id:
            messages = messages.filter(id__gt=after_id)

        # 상대가 보낸 메시지를 읽음 처리
        match.messages.exclude(sender=request.user).update(is_read=True)

        serializer = MessageSerializer(messages, many=True)
        return Response({'messages': serializer.data})

    def post(self, request, match_id):
        match = self.get_match(request.user, match_id)
        if not match:
            return Response({'error': '접근 권한 없음'}, status=403)

        content = request.data.get('content', '').strip()
        if not content:
            return Response({'error': '내용이 비어있음'}, status=400)

        msg = Message.objects.create(
            match=match, sender=request.user, content=content
        )
        return Response(MessageSerializer(msg).data, status=201)