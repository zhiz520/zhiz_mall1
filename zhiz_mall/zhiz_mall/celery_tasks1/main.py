from celery import Celery
import os


# 1.为celery的运行, 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhiz_mall.settings')

# 2.实例化celery, 参数1设置脚本路径
app = Celery('celery_tasks1')

# 3.通过配置文件设置broker
app.config_from_object('celery_tasks1.config')


# 4.设置celery自动检测任务包
app.autodiscover_tasks(['celery_tasks1.sms', 'celery_tasks1.email'])

# 使用celery -A celery_tasks1.main worker -l INFO   启动celery