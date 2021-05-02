from django.test import TestCase

import json
import datetime

# Create your tests here.
from django.test import TestCase, Client

from arts.models    import Art, Media, Paper, Material
from artists.models import Artist
from .models        import Location, Auction, AuctionArt

client = Client()

class AuctionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Artist.objects.create(
            id                = 1,
            name              = '무니원',
            profile_image_url = 'url.jpeg',
            introduction      = '아',
            description       = '야'
        )
        Media.objects.create(
            id   = 1,
            name = '회화'
        )
        Paper.objects.create(
            id   = 1,
            name = '종이'
        )
        Material.objects.create(
            id   = 1,
            name = '연필'
        )
        Art.objects.create(
            id            = 1,
            name          = '작품-1',
            price         = 10000,
            description   = '설명',
            height_cm     = 100,
            width_cm      = 100,
            release_date  = datetime.datetime(2021,1,1),
            thumbnail_url = '1.jpeg',
            views         = 0,
            is_sold       = False,
            artist_id     = 1,
            material_id   = 1,
            media_id      = 1,
            paper_id      = 1
        )
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
                                'artist'           : '무니원',
                                'artist_image_url' : 'url.jpeg',
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