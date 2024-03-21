from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


# user not logged in returns json data
class LoginRequiredJsonMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        return JsonResponse({'code': 400, 'errmsg': 'User not logged in'})