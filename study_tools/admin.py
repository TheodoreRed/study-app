from django.contrib import admin
from .models import FlashCard, StudySet

# Register your models here.
admin.site.register({FlashCard, StudySet})