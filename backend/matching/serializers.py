from rest_framework import serializers
from .models import Question, Answer, Message

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'option_a', 'option_b', 'order']
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'user',
            'question',
            'selected',
            'created_at',
        ]
        read_only_fields = ['user', 'created_at']
class MessageSerializer(serializers.ModelSerializer):
    sender_nickname = serializers.CharField(source='sender.nickname', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'match', 'sender', 'sender_nickname',
                  'content', 'is_read', 'created_at']
        read_only_fields = ['sender', 'is_read', 'created_at']