from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, UserLeavingMessageSerializer, UserAddressSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        添加商品收藏
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # serializer_class = UserFavSerializer
    # 取消全局jwt验证
    # todo Session token?
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 将retrive的查询不去查询id 而去查询goods_id 因为前端没有办法获取到pk
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    # 显示收藏详情
    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer

        return UserFavSerializer


class UserLeavingMessageViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                                viewsets.GenericViewSet):
    serializer_class = UserLeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


# class UserAddressViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
#                          mixins.CreateModelMixin,
#                          viewsets.GenericViewSet):
# 如果增删改查都有 则直接用viewsets.ModelViewSet
class UserAddressViewSet(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    """
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
