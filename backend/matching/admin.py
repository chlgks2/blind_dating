from django.contrib import admin
from .models import Question, Answer, FriendRequest, Match, Message, Payment

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'option_a', 'option_b', 'match_type', 'weight', 'order')
    list_editable = ('match_type', 'weight')  # 목록에서 바로 수정 가능

admin.site.register(Answer)
admin.site.register(FriendRequest)
admin.site.register(Match)
admin.site.register(Message)
admin.site.register(Payment)
