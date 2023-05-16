from django.db import models


class StudySet(models.Model):
    title = models.CharField(max_length=200)

class FlashCard(models.Model):
    study_set = models.ForeignKey(StudySet, on_delete=models.CASCADE)
    term = models.CharField(max_length=200)
    definition = models.CharField(max_length=200)