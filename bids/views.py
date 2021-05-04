from datetime import datetime

from django.views         import View
from django.http.response import JsonResponse

from .models import Auction, Bidding

class AuctionView(View):
    def get(self, request):
        try:
            date = request.GET.get('date', None)

            if not date:
                return JsonResponse({'MESSAGE' : 'INVALID DATE'}, status=400)

            date = datetime.strptime(date, '%Y-%m-%d').date()

            auctions = Auction.objects.filter(
                start_date__date__lte = date,
                end_date__date__gte   = date
            ).select_related('location').prefetch_related('art__artist')

            auctions = [
                {
                    'id'           : auction.id,
                    'location'     : auction.location.name,
                    'address'      : auction.location.address,
                    'phone_number' : auction.location.phone_number,
                    'site_url'     : auction.location.site_url,
                    'start_at'     : auction.start_date.strftime('%Y-%m-%d %H:%M'),
                    'end_at'       : auction.end_date.strftime('%Y-%m-%d %H:%M'),
                    'x'            : auction.location.latitude_x,
                    'y'            : auction.location.longitude_y,
                    'arts'         : [
                        {
                            'artist'           : art.artist.name,
                            'artist_image_url' : art.artist.profile_image_url,
                            'name'             : art.name,
                            'thumbnail_url'    : art.thumbnail_url,
                            'price'            : art.price,
                            'released_year'    : art.release_date.year,
                        } for art in auction.art.all()
                    ]
                } for auction in auctions
            ]

            return JsonResponse({'auctions' : auctions}, status=200)

        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE ERROR'}, status=400)

class BiddingView(View):
    def get(self, request):
        biddings = Bidding.objects \
            .filter(in_progress=True) \
            .select_related('art__artist') \
            .order_by('finish_at') \

        arts = [
            {
                'id'            : bidding.art.id,
                'thumbnail_url' : bidding.art.thumbnail_url,
                'title'         : bidding.art.name,
                'artist'        : bidding.art.artist.name,
                'finish_at'     : bidding.finish_at.strftime('%m-%d %H:%M'),
            } for bidding in biddings
        ]

        return JsonResponse({'arts' : arts}, status=200)