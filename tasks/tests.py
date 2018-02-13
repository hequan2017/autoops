
#
# producer: 任务发布者, 通过调用API向celery发布任务的程序
# celery beat: 任务调度, 根据配置文件发布定时任务
# worker: 实际执行任务的程序
# broker: 接受任务消息,存入队列再按顺序分发给worker执行
# backend: 存储结果的服务器



