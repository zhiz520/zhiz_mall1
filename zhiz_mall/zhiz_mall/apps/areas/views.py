from django.shortcuts import render
from django.views import View
from apps.areas.models import Area
from django.http import JsonResponse
from django.core.cache import cache

# Create your views here.
class AreaView(View):

    def get(self, request):
        # 查询缓存数据
        provinces_list = cache.get('province')
        # 如果没有则查找数据并存储数据
        if provinces_list is None:
        # 获取省份
            provinces = Area.objects.filter(parent=None)
            # 转换为字典
            provinces_list = []        
            for province in provinces:
                provinces_list.append({
                        'id': province.id,
                        'name': province.name
                    }
                )
            # 保存缓存数据
            cache.set('province', provinces_list, 24*3600)

        return JsonResponse({'cdoe': 0, 'errmsg': 'ok', 'province_list': provinces_list})
    

class SubAreaView(View):

    def get(self, request, id):
        # 查询数据
        data_list = cache.get('city'.format(id))
        if data_list is None:
            # 获取id查询信息
            up_level = Area.objects.get(id=id)
            down_level = up_level.subs.all()

            data_list = []
            for item in down_level:
                data_list.append({
                    'id': item.id,
                    'name': item.name
                })
            cache.set('city'.format(id), data_list, 3600*24)


        return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': data_list})

