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