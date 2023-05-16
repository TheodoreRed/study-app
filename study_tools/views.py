from rest_framework import viewsets
from .models import StudySet, FlashCard
from .serializers import StudySetSerializer, FlashCardSerializer


class StudySetViewSet(viewsets.ModelViewSet):
    serializer_class = StudySetSerializer

    def get_queryset(self):
        return StudySet.objects.filter(user=self.request.user)


class FlashCardViewSet(viewsets.ModelViewSet):
    serializer_class = FlashCardSerializer

    def get_queryset(self):
        return FlashCard.objects.filter(study_set__user=self.request.user)