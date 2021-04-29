from django.views         import View
from django.http.response import JsonResponse

from .models import Banner

class BannerView(View):
    def get(self, request):
        banners = [
            {
                'image_url' : banner.image_url,
                'link_url'  : banner.link_url,
                'text'      : banner.text
            } for banner in Banner.objects.all()
        ]

        return JsonResponse({'banners' : banners}, status=200)