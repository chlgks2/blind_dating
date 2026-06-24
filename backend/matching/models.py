from django.db import models

from django.conf import settings

# Create your models here.

class Question(models.Model):
    """A vs B 양자택일 질문 (스와이프 좌/우)"""

    SIMILAR = 'similar'
    COMPLEMENT = 'complement'
    NEUTRAL = 'neutral'
    MATCH_TYPE_CHOICES = [
        (SIMILAR, '같을수록 좋음'),
        (COMPLEMENT, '다를수록 좋음'),
        (NEUTRAL, '재미용'),
    ]

    option_a = models.CharField(max_length=50)   # 왼쪽 (예: 넷플)
    option_b = models.CharField(max_length=50)   # 오른쪽 (예: 유튜브)
    match_type = models.CharField(max_length=12, choices=MATCH_TYPE_CHOICES, default=SIMILAR)
    weight = models.FloatField(default=1.0)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.option_a} vs {self.option_b}'

class Answer(models.Model):
    """유저의 선택 (A 또는 B)"""
    CHOICE_A = 'A'
    CHOICE_B = 'B'
    CHOICE_CHOICES = [(CHOICE_A, 'A'), (CHOICE_B, 'B')]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='answers', on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected = models.CharField(max_length=1, choices=CHOICE_CHOICES)  # 'A' or 'B'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')  # 질문당 1개 답변

    def __str__(self):
        return f'{self.user.nickname} - Q{self.question.id}: {self.selected}'
    
class FriendRequest(models.Model):
    """친구요청 (한 방향)"""
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (PENDING, '대기중'),
        (ACCEPTED, '수락됨'),
        (REJECTED, '거절됨'),
    ]

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_requests',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='received_requests',
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')   # 같은 사람에게 중복 요청 방지

    def __str__(self):
        return f'{self.from_user.nickname} → {self.to_user.nickname} ({self.status})'


class Match(models.Model):
    """매칭 성립 (양방향 수락 완료). 채팅방의 기준이 됨."""
    user_a = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='matches_a', on_delete=models.CASCADE
    )
    user_b = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='matches_b', on_delete=models.CASCADE
    )
    # 결제 상태 (5단계에서 사용)
    user_a_paid = models.BooleanField(default=False)
    user_b_paid = models.BooleanField(default=False)
    is_chat_open = models.BooleanField(default=False)   # 둘 다 결제하면 True
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_a', 'user_b')

    def check_chat_open(self):
        """둘 다 결제했는지 확인해서 채팅 오픈 처리"""
        if self.user_a_paid and self.user_b_paid:
            self.is_chat_open = True
            self.save()
        return self.is_chat_open

class Message(models.Model):
    """매칭된 두 유저 간 메시지"""
    match = models.ForeignKey(
        Match, related_name='messages', on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']   # 오래된 순 정렬

    def __str__(self):
        return f'{self.sender.nickname}: {self.content[:20]}'
    
class Payment(models.Model):
    """결제 기록"""
    match = models.ForeignKey(Match, related_name='payments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imp_uid = models.CharField(max_length=100, unique=True)   # 포트원 결제 고유번호
    amount = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)