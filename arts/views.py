import json

from django.views import View
from django.http  import JsonResponse

from .models        import Art, Media
from artists.models import Artist

class ArtList(View):
    def get(self, request, media_id):

        try:
            offset     = int(request.GET.get('offset', 0))
            limit      = int(request.GET.get('limit', 5))
            min_price  = int(request.GET.get('min_price', 0))
            max_price  = int(request.GET.get('max_price', 99999999999))
            min_height = int(request.GET.get('min_height', 0))
            max_height = int(request.GET.get('max_height', 9999))
            min_width  = int(request.GET.get('min_width', 0))
            max_width  = int(request.GET.get('max_width', 9999))
            
            artists = Artist.objects.filter(
                    art__price__range     = (min_price, max_price),
                    art__height_cm__range = (min_height, max_height),
                    art__width_cm__range  = (min_width, max_width),
                    art__media_id         = media_id)
            
            artists_counts = list(set([artist.id for artist in artists]))

            filter_set = {'price__range'   : (min_price, max_price),
                        'height_cm__range' : (min_height, max_height),
                        'width_cm__range'  : (min_width, max_width),
                        'media_id'         : media_id}

            results = [
                {
                    'id'                : artist.id,
                    'name'              : artist.name,
                    'profile_image_url' : artist.profile_image_url,
                    'arts'              : list(Art.objects.filter(**filter_set, artist_id=artist.id)\
                                .values('id', 
                                    'thumbnail_url', 
                                    'price', 
                                    'height_cm', 
                                    'width_cm', 
                                    'material__name', 
                                    'paper__name'))
                                } for artist in artists[offset:offset+limit]
                    ]
            return JsonResponse({
                'MESSAGE'       : 'SUCCESS',
                'RESULT'        : results,
                'TOTAL_ARTISTS' : len(artists_counts)}, status=200)

        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE ERROR'}, status=400)
