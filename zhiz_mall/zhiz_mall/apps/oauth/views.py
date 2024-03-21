from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from zhiz_mall import settings


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