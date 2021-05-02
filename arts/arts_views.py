from django.views         import View
from django.http.response import JsonResponse

from .models import Banner, Art

class ArtDetailView(View):
    def get(self, request, art_id=None):
        if not Art.objects.filter(id=art_id).exists():
            return JsonResponse({'MESSAGE' : 'INVALID ART'}, status=404)

        art = Art.objects \
            .select_related('artist', 'status', 'paper', 'material') \
            .prefetch_related('artimage_set') \
            .get(id=art_id)

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
            'name'              : art.artist.name,
            'introduction'      : art.artist.introduction,
            'profile_image_url' : art.artist.profile_image_url,
            'description'       : art.artist.description
        }

        return JsonResponse({'art' : art_info, 'author' : author_info}, status=200)