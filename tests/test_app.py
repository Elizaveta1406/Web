import unittest
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Добро пожаловать в конвертер валют!'.encode('utf-8'), response.data)

    def test_successful_conversion(self):
        response = self.app.post('/', data=dict(
            amount='100',
            from_currency='RUB',
            to_currency='EUR'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('100.0 Российский рубль равно 1.0346708179900515 Евро'.encode('utf-8'), response.data)

    def test_invalid_input_non_numeric(self):
        response = self.app.post('/', data=dict(
            amount='abc',
            from_currency='RUB',
            to_currency='EUR'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Некорректный ввод. Введите положительное число.'.encode('utf-8'), response.data)

    def test_invalid_input_negative_number(self):
        response = self.app.post('/', data=dict(
            amount='-100',
            from_currency='RUB',
            to_currency='EUR'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Некорректный ввод. Введите положительное число.'.encode('utf-8'), response.data)

if __name__ == '__main__':
    unittest.main()