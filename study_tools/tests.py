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

    def test_post(self):
        data = {
            'title':'New Study Set',
            'description':'This is a new test description'
        }
        response = self.client.post('/api/studysets/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'New Study Set')
        self.assertEqual(response.data['description'], 'This is a new test description')

    def test_put(self):
        data = {
            'title':'World History',
            'description':'Even newer description'
        }
        response = self.client.put(f'/api/studysets/{self.study_set.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'World History')
        self.assertEqual(response.data['description'], 'Even newer description')

    def test_patch(self):
        data = {
            'description':'Even newer description'
        }
        response = self.client.patch(f'/api/studysets/{self.study_set.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.study_set.title)
        self.assertEqual(response.data['description'], 'Even newer description')

    def test_delete(self):
        response = self.client.delete(f'/api/studysets/{self.study_set.id}/')
        study_set_exists = StudySet.objects.filter(id=self.study_set.id).exists()
        self.assertEqual(response.status_code, 204)
        self.assertFalse(study_set_exists)

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

    def test_post(self):
        data = {
            'study_set':self.study_set.id,
            'term':'This is a new term',
            'definition':'New definition'
        }
        response = self.client.post('/api/flashcards/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['term'], 'This is a new term')
        self.assertEqual(response.data['definition'], "New definition")

    def test_put(self):
        data = {
            'study_set':self.study_set.id,
            'term':'Photosynthesis',
            'definition':'Energy from sun!'
        }
        response = self.client.put(f'/api/flashcards/{self.flashcard.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['term'], 'Photosynthesis')
        self.assertEqual(response.data['definition'], 'Energy from sun!')

    def test_patch(self):
        data = {
            'study_set':self.study_set.id,
            'definition':'the process by which green plants and some other organisms use sunlight to synthesize foods from carbon dioxide and water.'
        }
        response = self.client.patch(f'/api/flashcards/{self.flashcard.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['term'], self.flashcard.term)
        self.assertEqual(response.data['definition'], 'the process by which green plants and some other organisms use sunlight to synthesize foods from carbon dioxide and water.')

    def test_delete(self):
        response = self.client.delete(f'/api/flashcards/{self.flashcard.id}/')
        flashcard_exists = FlashCard.objects.filter(id=self.flashcard.id).exists()
        self.assertEqual(response.status_code, 204)
        self.assertFalse(flashcard_exists)


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
