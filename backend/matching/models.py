from django.db import models

from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50) 
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name
    

class Question(models.Model):
    SINGLE = 'single'
    MUTLI = 'multi'
    TYPE_CHOICES = [(SINGLE, '단일선택'),(MUTLI, '복수선택')]

    SIMILAR = 'similar'
    COMPLEMENT = 'complement'
    NEUTRAL = 'neutral'
    MATCH_TYPE_CHOICES = [
        (SIMILAR, '같을수록 좋음'),
        (COMPLEMENT, '다를수록 좋음'), # ex) 계획 짜주는 사람 계획 따라가는거 좋아하는사람 
        (NEUTRAL, '재미용'), # 민초파 vs 민초극혐파 이런식으로 재미용임 -> 가중치 작게
    ]

    category = models.ForeignKey(
        Category, related_name='questions', on_delete=models.CASCADE
    )
    text = models.TextField()
    q_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=SINGLE)
    match_type = models.CharField(max_length=12, choices=MATCH_TYPE_CHOICES, default=SIMILAR)
    weight = models.FloatField(default=1.0)       # 가중치 웨이트임
    order = models.IntegerField(default=0)

    parent_choice = models.ForeignKey(
        'choice',
        null=True,
        blank=True,
        related_name='follow_up_questions',
        on_delete=models.CASCADE
    )


    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:30]
    
class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name='choices', on_delete=models.CASCADE
    )
    text = models.TextField()
    value = models.IntegerField()  # 1, 2, 3 (분석용 코드)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.question.text} - {self.text}'

class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='answer',on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True)

    class Meta:
        unique_together = ('user', 'question', 'choice')

    def __str__(self):
        return f"{self.user} - {self.question.id} - {self.choice.value}"
    
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