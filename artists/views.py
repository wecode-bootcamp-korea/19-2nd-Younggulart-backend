from django.views         import View
from django.http.response import JsonResponse

from .models import Artist

class NewAritstsView(View):
    def get(self, request):
        ARTISTS_INDEX_SLICING = 4
        
        artists_new = Artist.objects.order_by('-created_at')[:ARTISTS_INDEX_SLICING]

        artists = [
            {
                'id'            : artist.id,
                'name'          : artist.name,
                'thumbnail_url' : artist.profile_image_url
            } for artist in artists_new
        ]
        
        return JsonResponse({'artists' : artists}, status=200)