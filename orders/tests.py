import json

from django.test import TestCase, Client

from .models     import FrameSize, FrameMaterial
from arts.models import Art

client = Client()

class FrameViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        FrameMaterial.objects.create(name             = 'Black wood',
                                     image_url        = '사진.jpg',
                                     render_image_url = '테두리.jpg')
        FrameSize.objects.create(name            = 'S',
                                 price_rise_rate = 1,
                                 thickness_cm    = 3)
        Art.objects.create(name          = '작품',
                           price         = 10000,
                           description   = '설명',
                           height_cm     = 150,
                           width_cm      = 100,
                           release_date  = '2021-05-05',
                           thumbnail_url = 'jpg',
                           views         = 0,
                           is_sold       = 0)

    def tearDown(self):
        FrameMaterial.objects.all().delete()
        FrameSize.objects.all().delete()
        Art.objects.all().delete()

    def test_frameview_success(self):
        response = client.get('/frame/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS',
            'sizes' : [{
                'size'  : 'S',
                'price' : '75900.000000',
                }],
            'materials' : [{
                'material'         : 'Black wood',
                'image_url'        : '사진.jpg',
                'render_image_url' : '테두리.jpg'
                }]
            })

    def test_frameview_value_error(self):
        response = client.get('/frame/22')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'MESSAGE' : 'ART DOES NOT EXIST'})
