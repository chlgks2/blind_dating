from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    AbstractUser가 username, password, email 등 기본 제공.
    소개팅에 필요한 필드만 추가.
    """

    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]

    nickname = models.CharField(max_length=30, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_year = models.IntegerField(null=True, blank=True)
    profile_image_url = models.URLField(max_length=500, null=True, blank=True)

    #질문 다풀었는지 물어보는거
    is_survey_done = models.BooleanField(default=False)

    # 매칭 선호도: similar(닮은사람) / complement(다른사람) / neutral(반반)
    MATCH_PREF_CHOICES = [
        ('similar', '비슷한 사람'),
        ('complement', '다른 사람'),
        ('neutral', '반반'),
    ]

    match_preference = models.CharField(
        max_length=12, choices=MATCH_PREF_CHOICES, default='neutral'
    )

    def __str__(self):
        return self.nickname

class AIJob(models.Model):
    """AI 이미지 변환 작업 (큐 역할)"""
    STYLE_CHOICES = [
        ('ghibli', '지브리'),
        ('anime2d', '2D 애니'),
        ('pixar', '픽사'),
        ('zepeto', '제페토'),
    ]
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('processing', '처리중'),
        ('done', '완료'),
        ('failed', '실패'),
    ]

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    style = models.CharField(max_length=10, choices=STYLE_CHOICES)
    original_url = models.URLField(max_length=500)   # S3 원본 URL
    generated_url = models.URLField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']