import json
import requests

from datetime import datetime, timedelta

from django.db            import transaction
from django.views         import View
from django.http.response import JsonResponse

from users.models import User
from arts.models  import Art
from .models      import Auction, Bidding, BiddingUser

from users.utils  import login_decorator

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

    @login_decorator
    def post(self, request, art_id=None):
        BIDDING_IN_PROGRESS_STATUS_ID = 1
        BIDDING_VALID_DURATION_DAYS   = 2
        try:
            user          = request.user
            data          = json.loads(request.body)
            offered_price = data['offered_price']
            access_token  = request.headers.get('Authorization')

            if not Art.objects.filter(id=art_id).exists():
                return JsonResponse({'MESSAGE' : 'INVALID ART'}, status=404)

            art = Art.objects.get(id=art_id)

            with transaction.atomic():
                bidding, created = art.bidding_set.get_or_create(
                    in_progress  = True,
                    defaults     = {
                        'finish_at' : datetime.now() + timedelta(days=BIDDING_VALID_DURATION_DAYS)
                    }
                )

                BiddingUser.objects.update_or_create(
                    user     = user, 
                    bidding  = bidding, 
                    defaults = {'price' : offered_price}
                )

                art.status_id = BIDDING_IN_PROGRESS_STATUS_ID
                art.save()

            response = requests.post(
                'https://kapi.kakao.com/v2/api/talk/memo/default/send',
                headers = {'Authorization' : f'Bearer {access_token}'},
                data    = {
                    "template_object" : json.dumps(
                        {
                            "object_type" : "feed",
                            "content"     : {
                                "title"       : f"{art.name} 입찰 완료",
                                "description" : f"나의 입찰가 : {offered_price}원",
                                "image_url"   : art.thumbnail_url,
                                "link"        : {
                                    "web_url" : "https://www.singulart.com/ko/"
                                }
                            },
                            "buttons" : [
                                {
                                    "title" : "경매 상황 보기",
                                    "link"  : {
                                        "web_url" : "https://www.singulart.com/ko/"
                                    }
                                }
                            ]
                        }
                    )
                }
            )

            failed_message = response.json().get('msg')
            
            if failed_message:
                return JsonResponse({'MESSAGE' : failed_message}, status=400)

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)