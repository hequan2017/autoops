#/usr/src/python3
# -*- coding: utf-8 -*-

import os
import djcelery

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'mo2+&!_l_7z0ty4%e75a#gdf%*&es4p6n$y90xk=18uao*&8*y'

DEBUG = True

ALLOWED_HOSTS = ['*', ]


INSTALLED_APPS = [
    'bootstrap3',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'asset',
    'db',
    'names',
    'tasks',
    'library',
    'djcelery',
    'kombu',
    'rest_framework',
    'rest_framework.authtoken',
    'guardian',
    'DjangoUeditor',
    'release',
    'xadmin',
    'crispy_forms',
    'reversion',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1

ROOT_URLCONF = 'autoops.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'autoops.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#      'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'autoops',
#         'USER': 'root',
#         'PASSWORD': '111111',
#         'HOST': '192.168.1.21',
#         'PORT': '3306',
#      }
# }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom User Auth model
# AUTH_USER_MODEL = 'names.User'



SESSION_ENGINE = 'django.contrib.sessions.backends.db'
LOGIN_URL = '/login.html'


LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True
USE_L10N = False  # 注意是False 配合下边时间格式
USE_TZ = False  # 如果只是内部使用的系统，这行建议为false，不然会有时区问题
DATETIME_FORMAT = 'Y-m-d H:i:s'  # suit在admin里设置时间的一个小bug。需要把时间格式指定一下
DATE_FORMAT = 'Y-m-d'



STATIC_URL = '/static/'
# STATIC_ROOT = '/opt/autoops/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


djcelery.setup_loader()
BROKER_URL = 'redis://127.0.0.1:6379/0'  #消息存储数据存储在仓库0

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend' # 指定 Backend
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


CELERY_TIMEZONE = 'Asia/Shanghai'

#CELERY_ALWAYS_EAGER = True   # 如果开启，Celery便以eager模式运行, 则task便不需要加delay运行

CELERY_IMPORTS = ('tasks.tasks',)
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  #这是使用了django-celery默认的数据库调度模型,任务执行周期都被存在你指定的orm数据库中



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',)
}



MEDIA_ROOT = os.path.join(BASE_DIR, 'upload/')
MEDIA_URL = '/upload/'  # 这个是在浏览器上访问该上传文件的url的前缀



Webssh_ip = '114.115.132.147'        ##WebSSH 软件的 访问IP,也就是本机外网IP，改这个地方就好了。
Webssh_port='9000'              ##端口号,默认即可。如有修改，也需要修改  webssh/main.py文件   define('port', default=9000, help='listen port', type=int)

Inception_ip = '127.0.0.1'                  ## 此为 Inception 软件地址,  默认为本机地址，一般不用修改
Inception_port = '6669'                     ## 此为 Inception 软件端口号



inception_remote_system_password='654321'            ## 设置回滚备份服务器相关参数，并同步修改一下 script/inc.cnf 里面的设置
inception_remote_system_user='root'
inception_remote_backup_port='3306'
inception_remote_backup_host='192.168.10.100'       ##备份数据库地址