import json
import bcrypt
import jwt

from django.shortcuts               import render, redirect
from django.views                   import View
from django.http                    import HttpResponse,JsonResponse
from django.core.mail               import EmailMessage, send_mail
from django.core                    import mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader         import render_to_string
from django.template                import loader
from django.utils.http              import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.exceptions         import ObjectDoesNotExist
from django.db                      import models
from django.views.decorators.csrf   import csrf_exempt
from django.utils.encoding          import force_text, force_bytes

from .tokens                        import user_activation_token
from per_eval                       import settings
from per_eval.settings              import SECRET_KEY, HASH
from .models                        import User, Department, UserQuestion
from eval.models                    import Question, Section
import my_settings                  

@csrf_exempt
def registration(request):
    if request.method == "POST":
        user = User.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            department_id = Department.objects.get(name=request.POST['department']).id,
            auth_id = 3
        )
        token = user_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk)).encode().decode()
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(user.id)).encode().decode()
        message = render_to_string('user/registration_verification.html',
                                   {'user'  : user,
                                   'domain' : current_site.domain,
                                   'uid'    : uid,
                                   'token'  : token,
                                  })
        url = build_verification_link(request,uid,token)
        send_mail(
        '인성평가 인증메일 입니다.',
        '',
        my_settings.EMAIL_HOST_USER,
        [user.email],
            html_message=render(request,'user/registration_verification.html',{'url':url}).content.decode('utf-8'))

        return HttpResponse(status = 200)

def build_verification_link(request,uid,token):
    return 'http://localhost:3000/activate?uid={}&token={}'.format(uid, token)

@csrf_exempt
def token_verification(request,**kwargs):
    if request.method == "POST":
        data = json.loads(request.body)
        id = force_text(urlsafe_base64_decode(data['uid']))
        token = data['token']
        user = User.objects.get(id = id)
        is_valid = user_activation_token.check_token(user,token)
        if is_valid:
            user.is_active = True
            user.save()
            return HttpResponse(status = 200)
        else:
            return HttpResponse(status = 403)

@csrf_exempt
def admin_signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
            if not User.objects.filter(email = data['email']).exists():
                password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())
                crypted = password.decode('utf-8')
                User.objects.create(
                    name  = data['name'],
                    password = crypted,
                    email = data['email'],
                    auth_id  = data['auth_id']
                )
                return HttpResponse(status = 200)
            return JsonResponse({ 'message' : 'DOES_EXIST' }, status = 400)
        except KeyError:
                return JsonResponse({ 'message' : 'IVALID_KEYS' },status = 400)

@csrf_exempt
def admin_signin(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email=data['email'])
                if bcrypt.checkpw(data['password'].encode('utf-8'),user.password.encode('utf-8')):
                    token  = jwt.encode({'email':data['email']}, SECRET_KEY, algorithm = HASH).decode('utf-8')
                    return JsonResponse({ 'token' : token }, status = 200)
                
                return JsonResponse({ 'message' : 'INVALID_USER' }, status = 401)
                    
            return JsonResponse({ 'message' : 'INVALID_USER' }, status = 401)
        
        except KeyError:
            return JsonResponse({ 'message' : 'INVALID_KEYS' }, status = 400)

