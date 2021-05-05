import json
import datetime

from django.test    import TestCase, Client
from unittest.mock  import MagicMock, patch

from arts.tests     import CustomTestCase

from artists.models import Artist
from users.models   import User
from arts.models    import Theme, Media, Art, ArtTheme, Paper, Material, ArtImage, ArtStatus
from .models        import Location, Auction, AuctionArt, Bidding

from my_settings    import KAKAO_TEST_TOKEN

client = Client()

class AuctionTest(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.make_artist_model_instances(cls)
        cls.make_art_model_instances(cls)

        Location.objects.create(
            id             = 1,
            name           = '장소',
            address        = '주소',
            phone_number   = '111-111-111',
            site_url       = None,
            operating_hour = '시간',
            latitude_x     = 127.0183737710409986,
            longitude_y    = 37.5128690375928002
        )
        Auction.objects.create(
            id          = 1,
            start_date  = datetime.datetime(2021,5,5),
            end_date    = datetime.datetime(2021,5,6),
            location_id = 1
        )
        AuctionArt.objects.create(
            id         = 1,
            art_id     = 1,
            auction_id = 1
        )

    def test_auctions_getby_date_success(self):
        self.maxDiff = None
        response     = client.get('/auctions?date=2021-5-6')

        self.assertEqual(response.json(),
            {
                'auctions' : [
                    {
                        'id' : 1,
                        'location'     : '장소',
                        'address'      : '주소',
                        'phone_number' : '111-111-111',
                        'site_url'     : None,
                        'start_at'     : '2021-05-05 00:00',
                        'end_at'       : '2021-05-06 00:00',
                        'x'            : '127.0183737710409986',
                        'y'            : '37.5128690375928002',
                        'arts' : [
                            {
                                'artist'           : '1',
                                'artist_image_url' : '1.jpeg',
                                'name'             : '작품-1',
                                'thumbnail_url'    : '1.jpeg',
                                'price'            : '10000.00',
                                'released_year'    : 2021
                            }
                        ]
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_auctions_getby_date_date_none(self):
        response = client.get('/auctions?date=')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['MESSAGE'], 'INVALID DATE')

    def test_auctions_getby_date_value_error(self):
        response = client.get('/auctions?date=2020년3월29일')

        self.assertEqual(response.status_code, 400)
        self.assertRaises(ValueError)
        self.assertEqual(response.json()['MESSAGE'], 'VALUE ERROR') 

class BiddingGetTest(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.make_artist_model_instances(cls)
        cls.make_art_model_instances(cls)
        Bidding.objects.create(id=1, art_id=1, finish_at=datetime.datetime(2021,1,1,1,1))
    
    def test_get_bidding_on_progress_success(self):
        response = client.get('/biddings/in-progress')

        self.assertEqual(response.json(),
            {
                "arts": [
                    {
                        "artist": "1",
                        "finish_at": "01-01 01:01",
                        "id": 1,
                        "thumbnail_url": "1.jpeg",
                        "title": "작품-1"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

class KaKaoMessagePostTest(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.make_artist_model_instances(cls)
        cls.make_art_model_instances(cls)
        cls.header = {
            'HTTP_Authorization' : KAKAO_TEST_TOKEN,
            'content_type'       : 'application/json'
        }
        cls.body = {'offered_price' : 10000}
        User.objects.create(email='msb925@naver.com')

    @patch('bids.views.requests')
    def test_kakao_message_success(self, mock_requests):
        class MockResponse :
            def json(self) : return {"result_code":0}

        mock_requests.post = MagicMock(return_value=MockResponse())

        response = client.post(
            '/biddings/1',
            json.dumps(self.body),
            **self.header
        )

    @patch('bids.views.requests')
    def test_kakao_message_sabotaged_template_fail(self, mock_requests):
        class MockResponse :
            def json(self) : return {"msg":"wrong template"}  

        mock_requests.post = MagicMock(return_value=MockResponse()) 

        response  = client.post(
            '/biddings/1',
            json.dumps(self.body),
            **self.header
        )

        self.assertEqual(response.status_code, 400)

    def test_kakao_message_invalid_art_fail(self):
        response = client.post(
            '/biddings/10990',
            json.dumps(self.body),
            **self.header
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),
            {
                'MESSAGE' : "INVALID ART"
            }
        )

    def test_kakao_message_key_error_fail(self):
        self.body = {'price' : 10}
        response  = client.post(
            '/biddings/1',
            json.dumps(self.body),
            **self.header
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'MESSAGE' : "KEY ERROR"
            }
        )