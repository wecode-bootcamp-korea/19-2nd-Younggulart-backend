import requests

from django.http.response import JsonResponse

from .models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)

        if not access_token:
            return JsonResponse({'MESSAGE' : 'UNAUTHORIZED ACCESS'}, status=401)

        response  = requests.get(
            'https://kapi.kakao.com/v2/user/me', 
            headers={'Authorization':f'Bearer {access_token}'}
        )

        user_email = response.json()['kakao_account']['email']

        if not User.objects.filter(email=user_email).exists():
            return JsonResponse({'MESSAGE' : 'INVALID USER'}, status=404)
            
        request.user = User.objects.get(email=user_email)

        return func(self, request, *args, **kwargs)

    return wrapper