from rest_framework import serializers
from .models import Category, Question, Choice, Answer

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'value', 'order']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only = True)
    category_name  = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Question
        fields = [
            'id', 'category', 'category_name', 'text',
            'q_type', 'match_type', 'weight', 'order',
            'parent_choice', 'choices',
        ]

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'user', 'question', 'choice', 'created_at']
        read_only_fields = ['user', 'created_at']
