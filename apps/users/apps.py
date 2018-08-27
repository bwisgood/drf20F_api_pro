from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    app_label = "用户"

    def ready(self):
        """
        型号量配置
        :return:
        """
        import users.signals