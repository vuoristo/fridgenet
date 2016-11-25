import unittest
from server import app

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_image_post(self):
        with open('./src/fixtures/dollar.jpg', 'rb') as f:
            image = f.read()
            response = self.app.post('/detect', data=image)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'tomato')


if __name__ == '__main__':
    unittest.main()
