from django.test import TestCase, RequestFactory


class TestIndexView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

