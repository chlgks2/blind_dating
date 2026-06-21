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