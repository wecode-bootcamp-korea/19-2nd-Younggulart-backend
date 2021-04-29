from django.views         import View
from django.http.response import JsonResponse

from artists.models import Type
from .models        import Banner, Media

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

class NavView(View):
    def get(self, request):
        NAV_ARTISTS_NUM = 2

        medium       = Media.objects.all()
        artist_types = Type.objects.all()

        arts = [
            {
                'media_name'  : media.name,
                'media_id'    : media.id,
                'media_image' : media.art_set.last().thumbnail_url,
                'themes'      : [
                    {
                        'theme_id'   : theme.id,
                        'theme_name' : theme.name
                    } for theme in media.theme_set.all()
                ]
            } for media in medium
        ]

        artists = [
            {
                'artist_type_name' : artist_type.name,
                'artist_type_id'   : artist_type.id,
                'representitives'  : [
                    {
                        'id'   : artist.id,
                        'name' : artist.name,
                        'profile_image' : artist.profile_image_url
                    } for artist in artist_type.artist_set.order_by('-created_at')[:NAV_ARTISTS_NUM]
                ]
            } for artist_type in artist_types
        ]

        return JsonResponse({'arts':arts, 'artists' : artists}, status=200)