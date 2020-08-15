import json
import requests
import jwt

from django.http import JsonResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .models import User
from my_settings import SECRET

def is_active(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            # token = kwargs.get('token')
            # uidb64 = kwargs.get('uidb64')
            uidb64 = request.headers.get('Authorization')
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = uid)
        except User.DoesNotExist:
            user = None
            return JsonResponse({'message' : 'INVALID_USER'})

        if user is not None and user.is_active == True:
            request.user = user
            return func(self, request, *args, **kwargs)
        else:
            return JsonResponse({'message' : 'INVALID_USER'})
    return wrapper

def user_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            payload = jwt.decode(token,SECRET['SECRET_KEY'], algorithms= 'HS256')
            user = User.objects.get(email = payload['email'])
            request.user = user
            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 400)
        
        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)
    return wrapper

            
