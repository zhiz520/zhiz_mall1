from libs.yuntongxun.sms import CCP
from celery_tasks1.main import app


# 生产者任务, 函数, 必须用celery实例装饰
@app.task
def celery_send_sms_code(mobile, code):
    CCP().send_template_sms(mobile, [code, 5], 1)