from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from zhiz_mall import settings
from apps.oauth.models import OAuthQQUser
from django.contrib.auth import login
import json
from apps.users.models import User
from utils.crypt1 import generate_encrypt, generate_decrypt


# Create your views here.
class QQLoginView(View):

    def get(self, request):
        # 1, Generating instance Objects
        oauth = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_url=settings.QQ_REDIRECT_URL,
            state='xxx'
        )
        qq_login_url = oauth.get_qq_url()
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'login_url': qq_login_url}) # 'login_url' 是配合前端写法
    

class OauthQQView(View):

    def get(self, request):
        # get code
        code = request.GET.get('code')
        if code is None:
            return JsonResponse({'code': 400, 'errmsg': 'Incomplete parameters'})
        # 2.Get token by code
        qq = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
            state='xxxx'
        )
        token = qq.get_access_token(code)
        # Get openid by token
        openid = qq.get_open_id(token)

        # Determine if a user is bound based on the poenid
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            crypt_openid = generate_encrypt(openid)
            response = JsonResponse({'code': 400, 'access_token': crypt_openid}) # 加密openid
        else:
            login(request, qquser.user)
            response = JsonResponse({'cdoe': 0, 'errmsg': 'ok'})
            response.set_cookie('username', qquser.user.username)
            return response
        
    def post(self, request):
        data = json.loads(request.body.decode())
        mobile = data.get('mobile')
        password = data.get('password')
        sms_code = data.get('sms_code')
        openid = generate_decrypt(data.get('access_token'))

        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)
        else:
            if user.check_password():
                return JsonResponse({'code': 400, 'errmsg': 'Incomplete parameters'})
        OAuthQQUser.objects.creat(user=user, openid=openid)

        login(request, user)

        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username)
        return response



        



