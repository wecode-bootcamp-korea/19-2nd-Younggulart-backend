
from django.db import connection
from django.views         import View
from django.http.response import JsonResponse

from .models import Banner, Art

class ArtDetailView(View):
    def get(self, request, art_id=None):
        art_id = art_id
        art    = Art.objects.filter(id=art_id) \
                            .select_related('artist') \
                            .prefetch_related('artimage_set') \
                            .first()

        if not art:
            return JsonResponse({'MESSAGE' : 'INVALID ART'}, status=404)

        artist = art.artist

        art_info = {
            'id'            : art.id,
            'name'          : art.name,
            'price'         : art.price,
            'description'   : art.description,
            'images'        : [
                image.image_url for image in art.artimage_set.all()
            ],
            'height_cm'     : art.height_cm,
            'width_cm'      : art.width_cm,
            'released_year' : art.release_date.strftime('%Y'),
            'status'        : art.status.name,
            'status_id'     : art.status.id,
            'author'        : art.artist.name,
            'material'      : art.material.name,
            'paper'         : art.paper.name,
        }

        author_info = {
            'name'              : artist.name,
            'introduction'      : artist.introduction,
            'profile_image_url' : artist.profile_image_url,
            'description'       : artist.description
        }
        print(len(connection.queries))
        return JsonResponse({'art' : art_info, 'author' : author_info}, status=200)