import json
import requests
import jwt

from django.http  import JsonResponse
from django.views import View

from .models     import User
from my_settings import SECRET_KEY, ALGORITHM

class KakaoLogin(View):
    def post(self, request):
        token = request.headers.get('Authorization', '')
        
        try:
            response  = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization':f'Bearer {token}'})
            user_info = response.json()

            user, created = User.objects.get_or_create(email=user_info['kakao_account']['email'])
            access_token  = jwt.encode({'user_id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
            
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'ACCESS_TOKEN' : access_token}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)
