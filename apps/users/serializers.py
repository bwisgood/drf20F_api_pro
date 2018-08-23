import re
import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model
from imooc_drf.settings import REGEX_MOBILE

from .models import VerifyCode

User = get_user_model()

class SmsSerializer(serializers.Serializer):
    """
    短信serializer
    """
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """

        # 验证手机号是否可以注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("手机号码已存在")
        # 验证手机号格式是否正确
        if not re.match(REGEX_MOBILE,mobile):
            raise serializers.ValidationError("手机号码非法")
        # 验证 验证码发送频率

        one_minute_ago = datetime.datetime.now() - datetime.timedelta(minutes=1)

        if not VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile):

            raise serializers.ValidationError("发送频率过快")

        return mobile


