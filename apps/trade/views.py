from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from trade.serializers import ShopCartSerializer, ShopCartListDetailSerializer
from .models import ShoppingCart


# Create your views here.

class ShopCartViewSet(viewsets.ModelViewSet):
    """
    购物车

    """
    # queryset = ShoppingCart.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # serializer_class = ShopCartSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartListDetailSerializer
        else:
            return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)
