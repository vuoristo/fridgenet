import unittest
from server import application
import json

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        application.config['TESTING'] = True
        self.app = application.test_client()

    # def test_image_post(self):
    #     with open('./src/fixtures/dollar.jpg', 'rb') as f:
    #         image = f.read()
    #         response = self.app.post('/detect', data=image)
    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(response.data, b'tomato')

    def test_inventory_get(self):
        response = self.app.get('/inventory')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(len(data), 2)


if __name__ == '__main__':
    unittest.main()
