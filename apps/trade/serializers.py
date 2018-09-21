from rest_framework import serializers

from trade.models import ShoppingCart
from goods.models import Goods
from goods.serializers import GoodsSerializer


class ShopCartListDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    nums = serializers.IntegerField(required=True, min_value=1, error_messages={
        "required": "数量不能缺少",
        "min_value": "最小不能小于一"
    })

    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())
    id = serializers.IntegerField(read_only=True)

    # 之所以在这里重写create方法 是因为我们想要用到serializer给我们提供的validate方法可以方便的校验参数，而且在文档中也是通过serializer来获取字段的
    def create(self, validated_data):
        user = self.context["request"].user
        goods = validated_data["goods"]
        nums = validated_data["nums"]

        exist = ShoppingCart.objects.filter(goods=goods, user=user).first()
        if exist:
            exist.nums += nums
            exist.save()
        else:
            exist = ShoppingCart.objects.create(**validated_data)
        return exist

    def update(self, instance, validated_data):
        nums = validated_data["nums"]
        instance.nums = nums
        instance.save()
        return instance
