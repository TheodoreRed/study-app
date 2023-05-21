from django.test import TestCase
from django.contrib.auth.models import User
from .models import StudySet, FlashCard
from django.db import IntegrityError
from rest_framework.test import APIClient, APITestCase

# simulate HTTP requests and assert the responses
class StudySetViewSetTest(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("testuser","test@email.com","testpassword")
        self.client.force_authenticate(user=self.user)
        self.study_set = StudySet.objects.create(user=self.user, title="History", description="This is the test description")

    def test_get(self):
        response = self.client.get('/api/studysets/')
        set_1 = response.data[0]
        self.assertEqual(set_1['title'], 'History')
        self.assertEqual(set_1['description'], 'This is the test description')
        self.assertEqual(set_1['user']['username'], 'testuser')
        self.assertEqual(response.status_code, 200)

class FlashcardViewSetTest(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.study_set = StudySet.objects.create(user=self.user, title="History", description="This is the test description")
        self.flashcard = FlashCard.objects.create(study_set=self.study_set, term="Test Term", definition="Test Definition")

    def test_get(self):
        response = self.client.get('/api/flashcards/')
        flashcard_1 = response.data[0]
        self.assertEqual(flashcard_1['term'], 'Test Term')
        self.assertEqual(flashcard_1['definition'], 'Test Definition')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)


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

    def test_term_uniqueness_within_same_study_set(self):
        
        with self.assertRaises(IntegrityError):
            FlashCard.objects.create(study_set=self.study_set, term=self.flash_card.term, definition="Different definition")
