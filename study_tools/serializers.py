from rest_framework import serializers
from .models import StudySet, FlashCard
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class FlashCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashCard
        fields = ['id', 'term', 'definition', 'date_of_creation']

class StudySetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # flashcards - all the flashcards related to a specific study set.
    flashcards = FlashCardSerializer(many=True, read_only=True)

    class Meta:
        model = StudySet
        fields = ['id', 'user', 'title', 'description', 'date_of_creation', 'flashcards']
