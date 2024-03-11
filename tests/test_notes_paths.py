from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import UserProfile


class TestView(TestCase):

    def setUp(self):
        User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.user = User.objects.get(id=1)
        UserProfile.objects.create(user=self.user)

    def test_home_path(self):
        response = self.client.get('/notes/')
        self.assertEqual(response.status_code, 200)

    def test_sections_path(self):
        response = self.client.get('/notes/sections/')
        self.assertEqual(response.status_code, 200)

    def test_by_section_path(self):
        response = self.client.get(reverse("notes:by_section", args=["Web Frameworks"]))
        self.assertEqual(response.status_code, 200)

    def test_detail_path(self):
        response = self.client.get('/notes/2/')
        self.assertEqual(response.status_code, 200)

    def test_edit_path(self):
        response = self.client.get('/notes/1/edit/')
        self.assertEqual(response.status_code, 200)

    def test_another_by_section_path(self):
        response = self.client.get(reverse("notes:by_section", args=["Setting up Django"]))
        self.assertEqual(response.status_code, 200)

    def test_vote_path(self):
        self.client.force_login(self.user)
        response = self.client.get('/notes/3/vote/')
        self.assertEqual(response.status_code, 200)
        
    def test_search_path(self):
        response = self.client.get('/notes/search/')
        self.assertEqual(response.status_code, 200)

    def test_added_ok_path(self):
        response = self.client.get('/notes/add/ok')
        self.assertEqual(response.status_code, 200)

    def test_add_path(self):
        response = self.client.get('/notes/add/')
        self.assertEqual(response.status_code, 200)


# python manage.py test tests.test_notes_paths