from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class StudySet(models.Model):
    user = models.ForeignKey(User, related_name='study_sets', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{}".format(self.title)

class FlashCard(models.Model):
    study_set = models.ForeignKey(StudySet, on_delete=models.CASCADE)
    term = models.CharField(max_length=200)
    definition = models.CharField(max_length=200)
    date_of_creation = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{}: {}".format(self.study_set, self.term)