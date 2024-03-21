from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from zhiz_mall import settings
from apps.oauth.models import OAuthQQUser
from django.contrib.auth import login

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
            response = JsonResponse({'code': 400, 'errmsg': 'user unbound'})
        else:
            login(request, qquser.user)
            response = JsonResponse({'cdoe': 0, 'errmsg': 'ok'})
            response.set_cookie('username', qquser.user.username)
            return response


