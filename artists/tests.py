import json
import datetime

from django.test    import TestCase, Client

from arts.tests     import CustomTestCase
from .models        import Artist

client = Client()

class ArtistsGetView(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        artists = cls.make_artist_model_instances(cls)['artists']
        artist_1 = artists[0]
        artist_1.created_at = datetime.datetime(2021,1,2)
        artist_1.save()

        artist_2 = artists[1]
        artist_2.created_at = datetime.datetime(2021,2,2)
        artist_2.save()
    
    def test_get_new_artists_success(self):
        response = client.get('/artists/new')

        self.assertEqual(response.json(),
            {
                "artists": [
                    {
                        "id"            : 2,
                        "name"          : "2",
                        "thumbnail_url" : "2.jpeg",
                    },
                    {
                        "id"            : 1,
                        "name"          : "1",
                        "thumbnail_url" : "1.jpeg",
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 200)