from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 기본 UserAdmin에 커스텀 필드 추가 표시
    list_display = ('username', 'nickname', 'gender', 'is_survey_done', 'match_preference')
    fieldsets = UserAdmin.fieldsets + (
        ('소개팅 정보', {'fields': ('nickname', 'gender', 'birth_year',
                                 'is_survey_done', 'match_preference')}),
    )
