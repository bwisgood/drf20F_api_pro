from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# 三级
from rest_framework import mixins
from rest_framework import generics
# 分页定制化
from rest_framework.pagination import PageNumberPagination
# 五阶 Viewset
from rest_framework import viewsets
# 使用django-filter过滤
from django_filters.rest_framework import DjangoFilterBackend
# 使用rest_framework的filter做搜索
from rest_framework import filters
# 配置单独的认证
from rest_framework.authentication import TokenAuthentication
# todo 配置jwt单独的认证

from .serializers import GoodsSerializer, CategorySerializer
from .models import Goods, GoodsCategory
from .filters import GoodsFilter


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    # queryset = Goods.objects.all().filter(category__parent_category__parent_category_id=1)
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # 使用django-filter过滤配置backends
    # 使用rest_framework的filter做搜索SearchFilter
    # 使用rest_framework的filter做排序OrderingFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 增加ordering_fields 需要排序的字段
    ordering_fields = ('sold_num', 'shop_price')
    # filter_fields
    # filter_fields = ('name','shop_price')
    # 自定义django-filter 将写好的filters.py中的filter配置到filter_class
    filter_class = GoodsFilter
    # 使用rest_framework的filter做搜索
    search_fields = ("name", 'goods_brief', 'goods_desc')
    # 将需要认证的view单独在view中声明
    # 公开数据
    # authentication_classes = (TokenAuthentication,)

    # filter过滤返回结果 重写默认的get_queryset方法
    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     # 获取get请求参数
    #     price_min = self.request.query_params.get("price_min", 0)
    #     if price_min:
    #         queryset = Goods.objects.filter(shop_price__gt=int(price_min))
    #     return queryset

    def post(self, request, format=None):
        """
        获取数据 创建good
        :param request:
        :param format:
        :return:
        """
        # request.data 可以方便获取到接收的参数 无论是GET POST BODY
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# class RetrieveMixView(viewsets.ViewSetMixin, generics.RetrieveAPIView):
#     pass


class CategoryListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.all()
    # queryset = GoodsCategory.objects.all()
    serializer_class = CategorySerializer
