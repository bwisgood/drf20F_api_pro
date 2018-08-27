import django_filters
# 是用django 的Q方法来过滤`或`条件
from django.db.models import Q
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    # 使用lookup_expr参数指定接收的参数在filters中的行为
    # drf更新 其中name更改为field_name
    pricemin = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    # 自定义过滤器方法添加method参数
    top_category = django_filters.NumberFilter(method='top_category_filter', field_name='category')

    def top_category_filter(self, queryset, name, value):
        """
        根据类目过滤商品
        :param queryset: 默认参数 GoodView中的queryset
        :param name: 默认参数
        :param value: 默认参数
        :return:
        """
        return queryset.filter(
            Q(category_id=value) | Q(category__parent_category_id=value) | Q(
                category__parent_category__parent_category_id=value))
    class Meta:
        model = Goods
        # 将字段加入fields
        fields = ['pricemin', 'pricemax', 'top_category', 'is_hot']


class CategoryFilter(django_filters.rest_framework.FilterSet):
    """
    商品类别的过滤类
    """
    pass
