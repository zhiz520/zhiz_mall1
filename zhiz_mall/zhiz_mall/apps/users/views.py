from inspect import modulesbyfile
import json
import re
from django.http import JsonResponse, SimpleCookie
from django.shortcuts import redirect, render
from django.views import View
from apps.users.models import User, Address
from django.contrib.auth import login, authenticate, logout
from utils.views1 import LoginRequiredJsonMixin
from django.core.mail import send_mail

from utils.crypt1 import generate_encrypt, generate_decrypt

from celery_tasks1.email.tasks import send_mail_celery

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
        
        if re.match(r'1[3-9]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'
        
        # verfication username and password
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '用户名或者密码错误'})
        
        # stay logged in
        else:
            login(request, user)
            print(request.user.is_authenticated)

        # Duration or state retention
        if remembered is None:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        # setting cookie infomation to display user infomation
        try:
            response.set_cookie('username', username, path='/')
        except Exception as e:
            print('出现错误：' , e)

        return response
        

class LoguotView(View):

    def delete(self, request):
        # deleting session infomation
        logout(request)
        # deletiong cookie infomation, because the previous section determines whather a user in logged in or not based on the cookie infomation
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.delete_cookie('username')
        return response


# User not logged in returns json data
class CenterView(LoginRequiredJsonMixin, View):

    def get(self, request):

        info_data = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': info_data})
    

class EmailView(LoginRequiredJsonMixin, View):

    def put(self, request):
        # 1.get data
        data = json.loads(request.body.decode())
        email = data.get('email')

        # 2, save e-mail address, request.user 是登陆用户的实例对象
        user = request.user
        user.email = email
        user.save()

        # 3.send verification email
        token = generate_encrypt(request.user.id)
        # send_mail(subject='bangdingyouxiang', 
        #           message='zhizhi', 
        #           from_email='3143433179@qq.com', 
        #           recipient_list=[email],
        #           html_message='点击按钮进行激活<a href="http://www.meisuo.site/?token={}>激活</a>'.format(token),
        #           )
        send_mail_celery.delay(
            subject='bangdingyouxiang', 
            message='zhizhi', 
            from_email='3143433179@qq.com', 
            recipient_list=[email],
            html_message='点击按钮进行激活<a href="http://www.meisuo.site/?token={}>激活</a>'.format(token),
        )
  
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class EmailVerifyView(View):

    def put(self, request):
        params = request.GET
        token = params.get('token')
        if token is None:
            return JsonResponse({'code': 400, 'errmsg': 'Incomplete parameters'})
        user_id = generate_decrypt(token)
        if user_id is None:
            return JsonResponse({'code': 400, 'errmsg': 'Incomplete parameters'})
        
        user = User.objects.get(id=user_id)
        user.email_active = True
        user.seve()

        return JsonResponse({'cdoe': 0, 'errmsg': 'ok'})
        
        

# 收货地址
class AddressCreateView(LoginRequiredJsonMixin, View):

    def post(self, request):
        # 1.get data
        data = json.loads(request.body.decode())
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')

        user = request.user
        # 2.验证必穿参数
        # if not all([receiver, ])

        # 3.参数入库
        address = Address.objects.create(
            user=user,
            title=receiver,
            receiver=receiver,
            province=province_id,
            city_id=city_id,
            district_id = district_id,
            place = place,
            mobile = mobile,
            tel = tel,
            email = email
        )

        # 4.返回响应
        address_dict = {
            'id': address.id,
            'title': address.title,
            'receiver': address.receiver,
            'province': address.province,
            'city': address.city,
            'district': address.district,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'address': address_dict})


