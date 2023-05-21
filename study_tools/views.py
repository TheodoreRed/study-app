from rest_framework import viewsets
from .models import StudySet, FlashCard
from .serializers import StudySetSerializer, FlashCardSerializer
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


class StudySetViewSet(viewsets.ModelViewSet):
    serializer_class = StudySetSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    # Filters StudySets to those owned by the authenticated user
    def get_queryset(self):
        return StudySet.objects.filter(user=self.request.user)
    
    # Sets current user as the owner of the StudySet
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FlashCardViewSet(viewsets.ModelViewSet):
    serializer_class = FlashCardSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    # Filters Flashcards to those owned by the authenticated user
    def get_queryset(self):
        return FlashCard.objects.filter(study_set__user=self.request.user)
    
    # Links new FlashCards to the specified StudySet
    def perform_create(self, serializer):
        study_set_id = self.request.data.get('study_set')
        if study_set_id:
            study_set = get_object_or_404(StudySet, id=study_set_id, user=self.request.user)
            serializer.save(study_set=study_set)
        else:
            raise ValidationError({'study_set':'This field is required!'})