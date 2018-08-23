from django.views.generic.base import View

from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        """
        获取商品列表页
        :param request:
        :return:
        """
        json_list = []
        goods = Goods.objects.all()[:10]
        # 可以将model转成一个dict
        from django.forms.models import model_to_dict

        # 这样直接json序列化会报错 json不能序列化datetimeField和imageField
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)

        import json
        from django.core import serializers
        json_data = serializers.serialize("json",goods)
        json_data = json.loads(json_data)

        from django.http import HttpResponse, JsonResponse
        # 为了序列化一个非数组对象，我们需要让safe这个参数设置为False 默认为True
        return JsonResponse(json_data, safe=False)
