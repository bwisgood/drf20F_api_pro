import re
import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model
from imooc_drf.settings import REGEX_MOBILE

from users.models import VerifyCode, UserProfile

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
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")
        # 验证 验证码发送频率

        one_minute_ago = datetime.datetime.now() - datetime.timedelta(minutes=1)

        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile):
            raise serializers.ValidationError("发送频率过快")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4, help_text="请输入验证码")

    def validate_code(self, code):
        code_record = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
        if code_record:
            code_record = code_record[0]
            five_minute_time = datetime.datetime.now() - datetime.timedelta(minutes=5)
            if code_record.add_time < five_minute_time:
                raise serializers.ValidationError("验证码过期")

            if code_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("未发送验证码")
            # 之所以不return 是因为我们保存用户时不需要将code保存到User中，User中也没有code字段
            # 只是用来做一个code的校验

    def validate(self, attrs):
        """
        在所有validate_[field]方法执行完后将会调用这个validate方法
        :param attrs: attrs是处理完所有的数据的集合
        :return:
        """
        # 将user的mobile字段设置为相同的username字段
        attrs["mobile"] = attrs["username"]
        # 删除attrs中我们不需要的code字段
        if attrs.get("code"):
            del attrs["code"]
        return attrs

    class Meta:
        model = UserProfile
        fields = ("username", "code", "mobile")
