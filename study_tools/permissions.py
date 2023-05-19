from rest_framework.permissions import BasePermission
from .models import StudySet, FlashCard


class IsOwner(BasePermission):
    """
    Custom permission class. Allows access only to owners of StudySet and FlashCard objects.
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, StudySet):
            return obj.user == request.user
        elif isinstance(obj, FlashCard):
            return obj.study_set.user == request.user