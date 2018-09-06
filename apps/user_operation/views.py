from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav
from .serializers import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    用户收藏功能
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    # 取消全局jwt验证
    # todo Session token?
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 将retrive的查询不去查询id 而去查询goods_id 因为前端没有办法获取到pk
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
