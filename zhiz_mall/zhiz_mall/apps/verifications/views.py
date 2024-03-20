from random import randint
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection

from libs.yuntongxun.sms import CCP

# Create your views here.
# Define the CAPTCHA 
class ImageCodeView(View):

    def get(self, request, uuid):
        # get image binary and captcha
        text, image = captcha.generate_captcha()
        # link to redis server
        redis_cli = get_redis_connection('code')
        # Storing CAPTCHA and UUID to redis database
        redis_cli.setex(uuid, 100, text)
        # return the image binary
        return HttpResponse(image, content_type='image/jpeg')


# Define Sms Verification code
class SmsCodeView(View):
     
     def get(self, request, mobile):
         # getting request paramters
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        # verification paramters
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': 'incomplete paramters'})
        # verification image code
        redis_cli = get_redis_connection('code')
        redis_image_code = redis_cli.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code': 400, 'errmsg': 'image code expired'})
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': 400, 'errmsg': 'image code err'})
        # generate image CAPTCHA
        sms_code = '%06d' %randint(0, 99999)
        redis_cli.setex(mobile, 300, sms_code)
        CCP().send_template_sms(mobile, [sms_code, 5], 1)
        return JsonResponse({'code': 0, 'errmsg': 'ok'})





