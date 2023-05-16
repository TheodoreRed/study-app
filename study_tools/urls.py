from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudySetViewSet, FlashCardViewSet

router = DefaultRouter()
router.register(r'studysets', StudySetViewSet, basename='studysets')
router.register(r'flashcards', FlashCardViewSet, basename='flashcards')

urlpatterns = [
    path('', include(router.urls)),
]