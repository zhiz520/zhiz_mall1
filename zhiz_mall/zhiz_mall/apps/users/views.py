import json
import re
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from apps.users.models import User
from django.contrib.auth import login, authenticate

# Create your views here.
# Determine if user name is duplicated
class UsernameCountView(View):

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})
        

# Define the registration calss
class RegisterView(View):

    def post(self, request):
        # Converted data
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        # get data
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')

        # Validation data
        if not all((username, password, password2, mobile, allow)):
            return JsonResponse({'code': 400, 'errmsg': 'Missing Required Parameters'})
        # Validation data rules
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({'code': 400, 'errmsg': 'Illegal username'})
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': 'Illegal password'})
        if password2 != password:
            return JsonResponse({'code': 400, 'errmsg': 'Inconsistent passwords'})
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': 'Illegal mobile number'})
        
        # data entry
        # user = User.objects.filter(username=username, password=password, mobile=mobile)
        # user.save()
        user = User.objects.create_user(username=username, password=password, mobile=mobile)
        print(user)
        login(request, user)
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
            

# setting up processing logic for logging in
class LoginView(View):

    def post(self, request):
        # receive data
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')

        # verification data
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        
        # verfication username and password
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '用户名或者密码错误'})
        
        # stay logged in
        login(request, user)

        # Duration or state retention
        if remembered is None:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        return JsonResponse({'code': 0, 'errmsg': 'ok'})
        

        