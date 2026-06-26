from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    # password는 받기만 하고 응답엔 안 보이게 write_only
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'nickname',
                  'gender', 'birth_year', 'match_preference']

    def create(self, validated_data):
        # create_user를 써야 비밀번호가 해시로 저장됨!
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
            gender=validated_data['gender'],
            birth_year=validated_data.get('birth_year'),
            match_preference=validated_data.get('match_preference', 'neutral'),
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """내 정보 조회용"""
    ai_image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'gender',
                  'birth_year', 'match_preference', 'is_survey_done', 'ai_image_url']

    def get_ai_image_url(self, obj):
        from .models import AIJob
        job = AIJob.objects.filter(user=obj, status='done').order_by('-created_at').first()
        return job.generated_url if job else None
