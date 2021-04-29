import json

from django.test import TestCase, Client

from .models import Banner

class BannerTest(TestCase):
    def setUp(self):
        client = Client()

        Banner.objects.create(
            id        = 2,
            image_url = 'https://bbbb.jpeg',
            link_url  = '#',
            text      = '블라'
        )

        Banner.objects.create(
            id        = 3,
            image_url = 'https://aaaa.jpeg',
            link_url  = '#',
            text      = '블'
        )

    def tearDown(self):
        Banner.objects.all().delete()

    def test_banners_get_success(self):
        client   = Client()
        response = client.get('/banners')
        self.assertEqual(response.json()['banners'][-1],
            {
                'link_url'  : '#',
                'image_url' : 'https://aaaa.jpeg',
                'text'      : '블'
            }
        )
        self.assertEqual(response.status_code, 200)