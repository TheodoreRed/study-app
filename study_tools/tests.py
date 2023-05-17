from django.test import TestCase
from django.contrib.auth.models import User
from .models import StudySet, FlashCard

class StudySetModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("testuser","test@email.com","testpassword")
        cls.study_set = StudySet.objects.create(user=cls.user, title="History", description="Study of the past.")

    def test_studyset_content(self):
        expected_title = self.study_set.title
        expected_description = self.study_set.description
        self.assertEqual(expected_title, "History")
        self.assertEqual(expected_description, "Study of the past.")


class FlashcardModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("testuser","test@email.com","testpassword")
        cls.study_set = StudySet.objects.create(user=cls.user, title="History", description="Study of the past.")
        cls.flash_card = FlashCard.objects.create(study_set=cls.study_set, term="Mesopotamia", definition="Land between Tigris and Euphrates rivers")

    def test_flashcard_content(self):
        expected_term = self.flash_card.term
        expected_definition = self.flash_card.definition
        self.assertEqual(expected_term, "Mesopotamia")
        self.assertEqual(expected_definition, "Land between Tigris and Euphrates rivers")

    def test_cascade_delete(self):
        self.study_set.delete()
        self.assertEqual(FlashCard.objects.filter(study_set=self.study_set).count(), 0)

    def test_related_name(self):
        self.assertEqual(self.study_set.flashcards.count(), 1)
        self.assertEqual(self.study_set.flashcards.first().term, "Mesopotamia")