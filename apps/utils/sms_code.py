import requests
import json


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "您的验证码是"
        }

        req_dict = requests.post(params=params, url=self.single_send_url)
        req_dict = json.loads(req_dict)

        return req_dict

    def send_sms_fake(self, code, mobile):
        return {"code": 0}
