from django.views import View
from django.http  import JsonResponse

from .models     import FrameMaterial, FrameSize
from arts.models import Art

class FrameView(View):
    def get(self, request, art_id):
        try:
            art   = Art.objects.get(id=art_id)
            price = lambda x, y, z, a : ((x + z) * (y + z) - (x * y)) * a * 100

            frame_sizes_prices = [
                {
                    'size'  : frame.name,
                    'price' : price(art.height_cm, art.width_cm, frame.thickness_cm, frame.price_rise_rate)
                    } for frame in FrameSize.objects.all()
                ]

            frame_materials = [
                {
                    'material'         : frame.name,
                    'image_url'        : frame.image_url,
                    'render_image_url' : frame.render_image_url
                    } for frame in FrameMaterial.objects.all()
                ]
            
            return JsonResponse({'MESSAGE'  : 'SUCCESS', 
                                 'SIZE'     : frame_sizes_prices, 
                                 'MATERIAL' : frame_materials}, status = 200)

        except Art.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'ART DOES NOT EXIST'}, status=404)
