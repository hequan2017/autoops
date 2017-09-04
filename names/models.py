from django.db import models

from django.contrib.auth.models import AbstractUser

# # Create your models here.
# __all__ = ['User',]
#
#
# class User(AbstractUser):
# 	ROLE_CHOICES = (
# 		('Admin', ('Administrator')),
# 		('User', ('User')),
# 		('App', ('Application'))
# 	)
# 	username = models.CharField(max_length=20, unique=True, verbose_name=('Username'))
# 	name = models.CharField(max_length=20, verbose_name=('Name'))
# 	email = models.EmailField(max_length=30, unique=True, verbose_name=('Email'))
# 	role = models.CharField(choices=ROLE_CHOICES, default='User', max_length=10, blank=True, verbose_name=('Role'))
# 	avatar = models.ImageField(upload_to="avatar", null=True, verbose_name=('Avatar'))
# 	wechat = models.CharField(max_length=30, blank=True, verbose_name=('Wechat'))
# 	phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=('Phone'))
#
#
# 	comment = models.TextField(max_length=200, blank=True, verbose_name=('Comment'))
# 	is_first_login = models.BooleanField(default=False)
# 	created_by = models.CharField(max_length=30, default='', verbose_name=('Created by'))




