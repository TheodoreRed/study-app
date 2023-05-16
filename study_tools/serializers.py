from rest_framework import serializers
from .models import StudySet, FlashCard
from django.contrib.auth.models import User

class FlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields = ['id', 'study_set', 'term', 'definition']

class StudySetSerializer(serializers.ModelSerializer):
    # 'flashcards' - nested representation of all the flashcards related to a specific study set.
    flashcards = FlashCardSerializer(many=True, read_only=True)

    class Meta:
        model = StudySet
        fields = ['id', 'title', 'flashcards']
