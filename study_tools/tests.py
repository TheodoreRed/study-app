from django.test import TestCase
from django.contrib.auth.models import User
from .models import StudySet, FlashCard
from django.db import IntegrityError
from rest_framework.test import APIClient, APITestCase
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED


class UserAuthTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create_user(username="testuser", email="testuser@test.com", password="testpassword")
        self.test_user.save()

    def test_user_registration_login_logout(self):

        # Test Registration
        data = {
            'username':'newuser',
            'password':'the_Yellow_Brick_Road',
        }
        response = self.client.post(f'/auth/users/', data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

        # Test Login
        response = self.client.post(f'/auth/token/login/', data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        token = response.data["auth_token"]
        self.assertIsNotNone(token)

        # Authenticate the user and logout
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token))
        response = self.client.post('/auth/token/logout/') # Logging out deletes the authetication token
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

        # Test the token has been deleted
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/studysets/')
        print(response.status_code, response.content)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

class PermissionTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="testuser1", password="testpassword1")
        self.user2 = User.objects.create_user(username="testuser2", password="testpassword2")
        self.study_set = StudySet.objects.create(user=self.user1, title="React", description="Javascript framework")
        self.flashcard = FlashCard.objects.create(study_set=self.study_set, term="DOM", definition="Document Object Model")
        self.client.force_authenticate(user=self.user1)

    def test_non_owner_cannot_access_studyset(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f'/api/study_set/{self.study_set.id}/')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_non_owner_cannot_access_flashcard(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f'/api/flashcard/{self.flashcard.id}/')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_unauthenticated_cannot_access_studyset(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/study_set/{self.study_set.id}/')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_unauthenticated_cannot_access_flashcard(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/flashcard/{self.flashcard.id}/')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

# simulate HTTP requests and assert the responses
class StudySetViewSetTest(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("testuser","test@email.com","testpassword")
        self.client.force_authenticate(user=self.user)
        self.study_set = StudySet.objects.create(user=self.user, title="History", description="This is the test description")

    def test_get(self):
        response = self.client.get(f'/api/studysets/')
        set_1 = response.data[0]
        self.assertEqual(set_1['title'], 'History')
        self.assertEqual(set_1['description'], 'This is the test description')
        self.assertEqual(set_1['user']['username'], 'testuser')
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_get_nonexistent(self):
        self.study_set.delete()
        response = self.client.get(f'/api/studysets/{self.study_set.id}/')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_post(self):
        data = {
            'title':'New Study Set',
            'description':'This is a new test description'
        }
        response = self.client.post(f'/api/studysets/', data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Study Set')
        self.assertEqual(response.data['description'], 'This is a new test description')
    
    def test_invalid_post(self):
        data = {
            'description':'This is a new test description'
        }
        response = self.client.post(f'/api/studysets/', data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

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
        response = self.client.get(f'/api/flashcards/')
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
        response = self.client.post(f'/api/flashcards/', data)
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

    def setUp(self):
        self.user = User.objects.create_user("testuser","test@email.com","testpassword")
        self.study_set = StudySet.objects.create(user=self.user, title="History", description="Study of the past.")

    def test_studyset_content(self):
        expected_title = self.study_set.title
        expected_description = self.study_set.description
        self.assertEqual(expected_title, "History")
        self.assertEqual(expected_description, "Study of the past.")


class FlashcardModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("testuser","test@email.com","testpassword")
        self.study_set = StudySet.objects.create(user=self.user, title="History", description="Study of the past.")
        self.flash_card = FlashCard.objects.create(study_set=self.study_set, term="Mesopotamia", definition="Land between Tigris and Euphrates rivers")

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
