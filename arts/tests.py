import json
import datetime

from django.test import TestCase, Client

from .models        import Banner, Theme, Media, Art, ArtTheme, Paper, Material, ArtImage, ArtStatus
from artists.models import Artist, Type, ArtistType

client = Client()

class CustomTestCase(TestCase):
    def make_artist_model_instances(self):
        artists = Artist.objects.bulk_create([
            Artist(
                id   = i,
                name = i,
                profile_image_url = f'{i}.jpeg',
                introduction = i,
                description  = i
            ) for i in range(1,3)
        ])

        types = Type.objects.bulk_create([
            Type(
                id   = i+1,
                name = v
            ) for i, v in enumerate(['화가', '사진가'])
        ])

        artist_types = ArtistType.objects.bulk_create([
            ArtistType(artist_id = i+1, type_id = i+1) for i in range(2)
        ])

        return {
            "artists" : artists,
            "types"   : types,
            "artist_types" : artist_types,
        }
    
    def make_art_model_instances(self):
        media = Media.objects.create(
            id   = 1,
            name = '회화'
        )

        theme1 = Theme.objects.create(
            id       = 1,
            name     = '거리미술',
            media_id = 1
        )

        theme2 = Theme.objects.create(
            id       = 2,
            name     = '대중문화',
            media_id = 1
        )

        paper = Paper.objects.create(
            id   = 1,
            name = '종이'
        )

        material = Material.objects.create(
            id   = 1,
            name = '연필'
        )

        art_status = ArtStatus.objects.create(id=1, name='입찰 완료')

        art1 = Art.objects.create(
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
            paper_id      = 1,
            status_id     = 1
        )

        art2 = Art.objects.create(
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
            paper_id      = 1,
            status_id     = 1
        )

        art_themes = ArtTheme.objects.bulk_create([
            ArtTheme(art_id=i+1, theme_id=i+1) for i in range(2)
        ])

        return {
            "media" : media,
            "themes" : [theme1, theme2],
            "paper" : paper,
            "material" : material,
            "arts" : [art1, art2],
            "art_status" : art_status,
            "art_themes" : art_themes
        }

class BannerTest(TestCase):
    def setUp(self):
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
        response = client.get('/banners')
        self.assertEqual(response.json()['banners'][-1],
            {
                'link_url'  : '#',
                'image_url' : 'https://aaaa.jpeg',
                'text'      : '블'
            }
        )
        self.assertEqual(response.status_code, 200)

class NavTest(CustomTestCase):
    def setUp(self):
        self.make_artist_model_instances()
        self.make_art_model_instances()

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
                                'profile_image': '1.jpeg'
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
                                'profile_image' : '2.jpeg'
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

class ArtDetailTest(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.make_artist_model_instances(ArtDetailTest)
        cls.make_art_model_instances(ArtDetailTest)

        ArtImage.objects.create(id=1, art_id=1, image_url='thumbnail.jpeg')
        ArtImage.objects.create(id=2, art_id=1, image_url='url.jpeg')

    def test_art_get_success(self):
        client   = Client()
        response = client.get('/arts/1')

        self.maxDiff = None
        self.assertEqual(response.json(),
            {
                'art': {
                    'id'            : 1,
                    'author'        : '1',
                    'description'   : '설명',
                    'height_cm'     : '100.00',
                    'width_cm'      : '100.00',
                    'images'        : ['thumbnail.jpeg','url.jpeg'],
                    'material'      : '연필',
                    'name'          : '작품-1',
                    'paper'         : '종이',
                    'price'         : '10000.00',
                    'released_year' : '2021',
                    'status'        : '입찰 완료',
                    'status_id'     : 1
                },
                'author': {
                    'description'       : '1',
                    'introduction'      : '1',
                    'name'              : '1',
                    'profile_image_url' : '1.jpeg'
                }
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_art_get_not_found(self):
        response = client.get('/arts/3')

        self.assertEqual(response.json(),{'MESSAGE' : 'INVALID ART'})
        self.assertEqual(response.status_code, 404)

class ArtListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        artist = Artist.objects.create(
                name = '이이', 
                profile_image_url = '사진.jpg',
                introduction = '소개',
                description = '설명')
        
        material = Material.objects.create(name='연필')
        paper    = Paper.objects.create(name='도화지')
        media    = Media.objects.create(name='회화')
        
        art = Art.objects.create(
                name          = '그림',
                price         = 5000,
                description   = '설명',
                thumbnail_url = 'jpg',
                height_cm     = 100,
                width_cm      = 100,
                release_date  = '2021-05-04',
                views         = 0,
                is_sold       = 0,
                artist        = artist,
                material      = material,
                media         = media,
                paper         = paper
                )
    
    def tearDown(self):
        Art.objects.all().delete()
        Media.objects.all().delete()
        Paper.objects.all().delete()
        Material.objects.all().delete()
        Artist.objects.all().delete()

    def test_artlist_success(self):
        response = client.get('/artlist/2')
        self.maxDiff = None
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE' : 'SUCCESS',
            'RESULT' : [{
                'id'                : 3,
                'name'              : '이이',
                'profile_image_url' : '사진.jpg',
                'arts'              : [{
                    'id'             : 3,
                    'thumbnail_url'  : 'jpg',
                    'price'          : '5000.00',
                    'height_cm'      : '100.00',
                    'width_cm'       : '100.00',
                    'material__name' : '연필',
                    'paper__name'    : '도화지'
                    }]
                }]
            })

    def test_artlist_value_error(self):
        response = client.get('/artlist/1?max_price=test')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE' : 'VALUE ERROR'})
