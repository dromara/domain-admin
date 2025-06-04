import unittest
from unittest.mock import patch, MagicMock
from domain_admin.main import create_app

class TestDomainCheck(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_check_domain_no_url(self):
        """测试未提供URL参数的情况"""
        response = self.client.get('/api/v1/domain/check')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 202)
        self.assertEqual(data['msg'], '请传入URL参数')

    @patch('requests.get')
    def test_check_domain_blocked(self, mock_get):
        """测试域名被封的情况"""
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'ok'}
        mock_get.return_value = mock_response

        response = self.client.get('/api/v1/domain/check?url=http://example.com')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 202)
        self.assertEqual(data['msg'], '域名被封')

    @patch('requests.get')
    def test_check_domain_normal(self, mock_get):
        """测试域名正常的情况"""
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'normal'}
        mock_get.return_value = mock_response

        response = self.client.get('/api/v1/domain/check?url=http://example.com')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 200)
        self.assertEqual(data['msg'], 'normal')

    @patch('requests.get')
    def test_check_domain_request_error(self, mock_get):
        """测试请求异常的情况"""
        mock_get.side_effect = requests.exceptions.RequestException('Connection error')

        response = self.client.get('/api/v1/domain/check?url=http://example.com')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 500)
        self.assertTrue('检测失败' in data['msg'])

    @patch('requests.get')
    def test_check_domain_json_error(self, mock_get):
        """测试JSON解析错误的情况"""
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError('Invalid JSON')
        mock_get.return_value = mock_response

        response = self.client.get('/api/v1/domain/check?url=http://example.com')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['code'], 500)
        self.assertEqual(data['msg'], '接口响应解析失败')

if __name__ == '__main__':
    unittest.main() 