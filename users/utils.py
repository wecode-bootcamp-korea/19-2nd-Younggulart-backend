import jwt

from django.http.response import JsonResponse

from .models     import User
from my_settings import SECRET_KEY, ALGORITHM

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)

            if not access_token:
                return JsonResponse({'MESSAGE' : 'UNAUTHORIZED'}, status=401)
            
            payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user    = User.objects.filter(user_id=payload['user_id']).first()

            if not user:
                return JsonResponse({'MESSAGE' : 'INVALID USER'}, status=404)
            
            request.user = user
            
            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE' : 'INVALID TOKEN'}, status=400)

    return wrapper