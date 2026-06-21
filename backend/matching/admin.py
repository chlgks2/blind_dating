from django.contrib import admin
from .models import Category, Question, Choice, Answer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3   # 기본 3칸 (1,2,3 선택지)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'text', 'q_type', 'match_type', 'weight')
    list_filter = ('category', 'q_type', 'match_type')
    inlines = [ChoiceInline]   # 질문 안에서 선택지 바로 입력


admin.site.register(Category)
admin.site.register(Answer)
