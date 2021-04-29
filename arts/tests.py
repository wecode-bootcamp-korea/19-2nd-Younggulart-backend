import json
import datetime

from django.test import TestCase, Client

from .models        import Banner, Theme, Media, Art, ArtTheme, Paper, Material
from artists.models import Artist, Type, ArtistType

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

class NavTest(TestCase):
    def setUp(self):
        client = Client()

        artists = [
            Artist(
                id   = i,
                name = i,
                profile_image_url = f'https://{i}.jpeg',
                introduction = i,
                description  = i
            ) for i in range(1,3)
        ]

        Artist.objects.bulk_create(artists)

        types = [
            Type(
                id   = i+1,
                name = v
            ) for i, v in enumerate(['화가', '사진가'])
        ]

        Type.objects.bulk_create(types)

        ArtistType.objects.bulk_create([ArtistType(artist_id = i+1, type_id = i+1) for i in range(2)])

        Media.objects.create(
            id   = 1,
            name = '회화'
        )

        Theme.objects.create(
            id       = 1,
            name     = '거리미술',
            media_id = 1
        )

        Theme.objects.create(
            id       = 2,
            name     = '대중문화',
            media_id = 1
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
            views         = 1,
            is_sold       = False,
            artist_id     = 1,
            material_id   = 1,
            media_id      = 1,
            paper_id      = 1
        )

        Art.objects.create(
            id            = 2,
            name          = '작품-2',
            price         = 50000,
            description   = '설명-2',
            height_cm     = 100,
            width_cm      = 100,
            release_date  = datetime.datetime(2021,1,1),
            thumbnail_url = '2.jpeg',
            views         = 1,
            is_sold       = False,
            artist_id     = 2,
            material_id   = 1,
            media_id      = 1,
            paper_id      = 1
        )

        ArtTheme.objects.bulk_create([ArtTheme(art_id=i+1, theme_id=i+1) for i in range(2)])

    def tearDown(self):
        ArtistType.objects.all().delete()
        ArtTheme.objects.all().delete()
        Art.objects.all().delete()
        Type.objects.all().delete()
        Artist.objects.all().delete()
        Paper.objects.all().delete()
        Theme.objects.all().delete()
        Media.objects.all().delete()
        Material.objects.all().delete()

    def test_banners_get_success(self):
        client   = Client()
        response = client.get('/nav')
        self.assertEqual(response.json(),
            {
                'artists': [
                    {
                        'artist_type_id'   : 1,
                        'artist_type_name' : '화가',
                        'representitives'  : [
                            {
                                'id': 1,
                                'name': '1',
                                'profile_image': 'https://1.jpeg'
                            }
                        ]
                    },
                    {
                        'artist_type_id'   : 2,
                        'artist_type_name' : '사진가',
                        'representitives' : [
                            {
                                'id'            : 2,
                                'name'          : '2',
                                'profile_image' : 'https://2.jpeg'
                            }
                        ]
                    }
                ],
                'arts': [
                    {
                        'media_id': 1,
                        'media_image': '2.jpeg',
                        'media_name': '회화',
                        'themes': [
                            {'theme_id' : 1, 'theme_name' : '거리미술'},
                            {'theme_id' : 2, 'theme_name' : '대중문화'}
                        ]
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)