import json
import jwt

from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

from .models     import User
from my_settings import SECRET_KEY, ALGORITHM

client = Client()

class KakaoLoginTest(TestCase):
    def setUp(self):
        User.objects.create(email='aaa@gmail.com')

    def tearDown(self):
        User.objects.all().delete()

    @patch('users.views.requests')
    def test_kakaologin_success(self, mock_requests):
        class MockResponse:
            def json(self):
                return {
                        'kakao_account' : {
                            'email'     : 'ccc@gmail.com'
                            }
                        }

        mock_requests.get = MagicMock(return_value=MockResponse())

        header   = {'HTTP_Authorization' : 'ACCESS_TOKEN'}
        response = client.post('/users/login/kakao', content_type='application/json', **header)
        
        access_token  = jwt.encode(
                {'user_id' : User.objects.get(email='ccc@gmail.com').id},
                SECRET_KEY, 
                algorithm=ALGORITHM
                ) 
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE' : 'SUCCESS', 'ACCESS_TOKEN' : access_token})

        @patch('users.views.requests')
        def test_kakaologin_keyerror(self, mock_requests):
            class MockResponse:
                def json(self):
                    return{
                              'account' : {
                                'email' : 'bbb@gmail.com'
                                }
                            }

            mock_requests.get = MagicMock(return_value=MockResponse())

            header   = {'HTTP_Authorization' : 'ACCESS_TOKEN'}
            response = client.post('/users/login/kakao', content_type='application/json', **header)

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {'MESSAGE' : 'KEY ERROR'})
