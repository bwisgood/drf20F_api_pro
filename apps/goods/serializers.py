from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsImage


class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    商品分类的Serializer
    """
    # 加上many
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    # 显示外键需要先创建外键的Serializer 然后覆盖ModelSerializer中的外键值
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        # fields = ("name","click_num","add_time")
        fields = "__all__"
