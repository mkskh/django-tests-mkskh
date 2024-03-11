from django.test import TestCase


class TestView(TestCase):

    def test_home_path(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_path(self):
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout_path(self):
        response = self.client.get('/user/logout/')
        self.assertEqual(response.status_code, 302)

        redirect_target = response.url
        expected_target = '/'
        self.assertEqual(redirect_target, expected_target)

        response_redirected_url = self.client.get(redirect_target)
        self.assertEqual(response_redirected_url.status_code, 200)

    def test_redirect_note_detail_path(self):
        response = self.client.get('/3/')
        self.assertEqual(response.status_code, 302)

        redirect_target = response.url
        expected_target = '/notes/3/'
        self.assertEqual(redirect_target, expected_target)

        response_redirected_url = self.client.get(redirect_target)
        self.assertEqual(response_redirected_url.status_code, 200)


# python manage.py test tests.test_paths