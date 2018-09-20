"""imooc_drf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
import xadmin
from imooc_drf.settings import MEDIA_ROOT
from django.views.static import serve
# drf
from rest_framework.documentation import include_docs_urls

from goods.views import GoodsListViewSet, CategoryListViewSet
from users.views import SmsViewSet, UserRegViewSet
from user_operation.views import UserFavViewSet, UserLeavingMessageViewSet, UserAddressViewSet
from trade.views import ShopCartViewSet
# 五阶 viewSet 配置路由
# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })

# 六阶 配置router
from rest_framework.routers import DefaultRouter
# 配置获取token 的api
from rest_framework.authtoken import views
# jwt导入url
from rest_framework_jwt.views import obtain_jwt_token

# 六阶 配置router
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name="goods_list")
router.register(r'categorys', CategoryListViewSet, base_name="categorys")
router.register(r'codes', SmsViewSet, base_name="codes")
router.register(r'users', UserRegViewSet, base_name="users")
router.register(r'userfavs', UserFavViewSet, base_name="userfavs")
router.register(r'messages', UserLeavingMessageViewSet, base_name="messages")
router.register(r'address', UserAddressViewSet, base_name="address")
router.register(r'carts', ShopCartViewSet, base_name="carts")

print(router.urls)
# 配置单条信息获取
category_one = CategoryListViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 商品列表页
    # 六阶 注释原有的goods获取路由
    # url(r'goods/$', goods_list, name="goods_list"),
    # 六阶 新增所有router配置
    url(r"^", include(router.urls)),
    url(r"^categorys/(?P<pk>[0-9]+)/$", category_one, name="single_info"),
    url(r"^docs/", include_docs_urls(title="bw")),
    # 配置获取token 的api地址
    # drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt的认证接口
    url(r"^login/", obtain_jwt_token)
]
